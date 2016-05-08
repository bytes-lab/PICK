from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.conf import settings
from django.test.utils import override_settings
from django.utils.encoding import force_text

from rest_framework import status

from .test_base import BaseAPITestCase
from order.models import *

class APITestCase(TestCase, BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    USERNAME = 'person'
    PASS = 'person'
    EMAIL = "person1@world.com"
    NEW_PASS = 'new-test-pass'
    REGISTRATION_VIEW = 'rest_auth.runtests.RegistrationView'

    # data without user profile
    REGISTRATION_DATA = {
        "email": EMAIL,
        "password1": PASS,
        "password2": PASS
    }

    REGISTRATION_DATA_WITH_EMAIL = REGISTRATION_DATA.copy()
    REGISTRATION_DATA_WITH_EMAIL['email'] = EMAIL

    BASIC_USER_DATA = {
        'first_name': "John",
        'last_name': 'Smith',
        'email': EMAIL,
        'address': 'Sydney Australia',
        'phone': '12025688404',
        'store_url': 'mel-restaurant.com',
        'package_type': 'Food',
        'gender': 'Male',
    }

    BASIC_ORDER_DATA = {
        'pickup_addr': 'ottawa, Canada',
        'contact_name': 'Waff Jason',
        'phone': '12025688555',
        'pickup_time': '2016-05-08 10:23 PM',
        'dropoff_time': '2016-05-09 11:13 AM',        
        'payment_type': 'COD',
    }

    USER_DATA = BASIC_USER_DATA.copy()
    USER_DATA['newsletter_subscribe'] = True

    def setUp(self):
        self.init()

    def _generate_uid_and_token(self, user):
        result = {}
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode

        result['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        result['token'] = default_token_generator.make_token(user)
        return result

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_login(self):
        payload = {
            "username": self.USERNAME,
            "email": self.EMAIL,
            "password": self.PASS
        }

        # there is no users in db so it should throw error (400)
        self.post(self.login_url, data=payload, status_code=400)

        self.post(self.password_change_url, status_code=403)

        # create user
        # user = get_user_model().objects.create_user('', self.EMAIL, self.PASS)
        user = get_user_model().objects.create_user(self.USERNAME ,self.EMAIL, self.PASS)

        self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual('key' in self.response.json.keys(), True)
        self.token = self.response.json['key']

        self.post(self.password_change_url, status_code=400)

        # test wrong username/password
        payload = {
            "email": self.EMAIL + '?',
            "password": self.PASS+'asdasd'
        }
        self.post(self.login_url, data=payload, status_code=400)

        # test empty payload
        self.post(self.login_url, data={}, status_code=400)

        # test inactive user
        user.is_active = False
        user.save()
        self.post(self.login_url, data=payload, status_code=403)


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_login_by_email(self):
        # starting test without allauth app
        settings.INSTALLED_APPS.remove('allauth')

        payload = {
            "email": self.EMAIL.lower(),
            "password": self.PASS
        }
        # there is no users in db so it should throw error (400)
        self.post(self.login_url, data=payload, status_code=400)

        self.post(self.password_change_url, status_code=403)

        # create user
        user = get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)

        # test auth by email
        self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual('key' in self.response.json.keys(), True)
        self.token = self.response.json['key']

        # test auth by email in different case
        payload = {
            "email": self.EMAIL.upper(),
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual('key' in self.response.json.keys(), True)
        self.token = self.response.json['key']

        # test wrong email/password
        payload = {
            "email": 't' + self.EMAIL,
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=400)

        # test empty payload
        self.post(self.login_url, data={}, status_code=400)

        # test inactive user
        user.is_active = False
        user.save()
        self.post(self.login_url, data=payload, status_code=403)


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_password_change(self):
        login_payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }
        get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)
        self.post(self.login_url, data=login_payload, status_code=200)
        self.token = self.response.json['key']

        # print self.token, '@@@@@@22'
        new_password_payload = {
            "new_password1": "new_person",
            "new_password2": "new_person"
        }

        # pass1 and pass2 are not equal
        new_password_payload = {
            "new_password1": "new_person1",
            "new_password2": "new_person"
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=400
        )

        # send empty payload
        self.post(self.password_change_url, data={}, status_code=400)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_password_change_with_old_password(self):
        login_payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }
        get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)
        self.post(self.login_url, data=login_payload, status_code=200)
        self.token = self.response.json['key']

        new_password_payload = {
            "old_password": "%s!" % self.PASS,  # wrong password
            "new_password1": "new_person",
            "new_password2": "new_person"
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=400
        )


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_password_reset_with_email_in_different_case(self):
        get_user_model().objects.create_user(self.USERNAME, self.EMAIL.lower(), self.PASS)

        # call password reset in upper case
        mail_count = len(mail.outbox)
        payload = {'email': self.EMAIL.upper()+'kjkjkj'}
        self.post(self.password_reset_url, data=payload, status_code=200)
        self.assertEqual(len(mail.outbox), mail_count)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_password_reset_with_invalid_email(self):
        """
        Invalid email should not raise error, as this would leak users
        """
        get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)

        # call password reset
        mail_count = len(mail.outbox)
        payload = {'email': 'nonexisting@email.com'}
        self.post(self.password_reset_url, data=payload, status_code=200)
        self.assertEqual(len(mail.outbox), mail_count)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_user_details(self):
        user = get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)
        payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=200)
        self.token = self.response.json['key']
        self.get(self.user_url, status_code=200)

        self.patch(self.user_url, data=self.BASIC_USER_DATA, status_code=200)
        user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(user.first_name, self.response.json['first_name'])
        self.assertEqual(user.last_name, self.response.json['last_name'])
        self.assertEqual(user.email, self.response.json['email'])
        self.assertEqual(user.phone, self.response.json['phone'])
        self.assertEqual(user.address, self.response.json['address'])
        self.assertEqual(user.store_url, self.response.json['store_url'])
        self.assertEqual(user.gender, self.response.json['gender'])
        self.assertEqual(user.package_type, self.response.json['package_type'])


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_registration(self):
        user_count = get_user_model().objects.all().count()

        # test empty payload
        self.post(self.register_url, data={}, status_code=400)

        result = self.post(self.register_url, data=self.REGISTRATION_DATA, status_code=201)
        self.assertIn('key', result.data)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)

        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.email, self.REGISTRATION_DATA['email'])

        self._login()
        self._logout()


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_registration_with_invalid_password(self):
        data = self.REGISTRATION_DATA.copy()
        data['password2'] = 'foobar'

        self.post(self.register_url, data=data, status_code=400)


    def test_registration_with_email_verification(self):
        user_count = get_user_model().objects.all().count()
        mail_count = len(mail.outbox)

        # test empty payload
        self.post(
            self.register_url,
            data={},
            status_code=status.HTTP_400_BAD_REQUEST
        )

        result = self.post(
            self.register_url,
            data=self.REGISTRATION_DATA_WITH_EMAIL,
            status_code=status.HTTP_201_CREATED
        )
        self.assertNotIn('key', result.data)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)
        self.assertEqual(len(mail.outbox), mail_count + 1)
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.email, self.REGISTRATION_DATA['email'])

        # email is not verified yet
        payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }
        self.post(
            self.login_url,
            data=payload,
            status=status.HTTP_400_BAD_REQUEST
        )

        # verify email
        email_confirmation = new_user.emailaddress_set.get(email=self.EMAIL)\
            .emailconfirmation_set.order_by('-created')[0]
        self.post(
            self.veirfy_email_url,
            data={"key": email_confirmation.key},
            status_code=status.HTTP_200_OK
        )

        # try to login again
        self._login()
        self._logout()


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    @override_settings(ACCOUNT_LOGOUT_ON_GET=True)
    def test_logout_on_get(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }

        # create user
        get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)

        self.post(self.login_url, data=payload, status_code=200)
        self.get(self.logout_url, status=status.HTTP_200_OK)


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')    
    @override_settings(ACCOUNT_LOGOUT_ON_GET=False)
    def test_logout_on_post_only(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }

        # create user
        get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)

        self.post(self.login_url, data=payload, status_code=status.HTTP_200_OK)
        self.get(self.logout_url, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


    @override_settings(ACCOUNT_EMAIL_VERIFICATION='optional')
    def test_orders(self):
        self.get(self.order_url, status_code=403)
        user = get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)
        payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }
        
        self.post(self.login_url, data=payload, status_code=200)
        self.token = self.response.json['key']
        self.get(self.order_url, status_code=200)

        self.post(self.order_url, data=self.BASIC_ORDER_DATA, status_code=201)

        self.assertEqual(user.email, self.response.json['owner'])
        self.assertEqual(self.BASIC_ORDER_DATA['pickup_addr'], self.response.json['pickup_addr'])
        self.assertEqual(self.BASIC_ORDER_DATA['contact_name'], self.response.json['contact_name'])
        self.assertEqual(self.BASIC_ORDER_DATA['phone'], self.response.json['phone'])
        self.assertEqual(self.BASIC_ORDER_DATA['pickup_time'], self.response.json['pickup_time'])
        self.assertEqual(self.BASIC_ORDER_DATA['dropoff_time'], self.response.json['dropoff_time'])
        self.assertEqual(user.package_type, self.response.json['items'])
        self.assertEqual(self.BASIC_ORDER_DATA['payment_type'], self.response.json['payment_type'])
        self.assertEqual('Initial', self.response.json['status'])
