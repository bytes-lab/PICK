from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from order.models import ITEMS

GENDER = (
	('Male', 'Male'),
	('Female', 'Female')
)

class Sender(AbstractUser):
    """
    Custom user class - Sender.
    """
    address = models.CharField(max_length=300)		# default location
    phone = models.CharField(max_length=50)
    store_url = models.CharField(max_length=50)
    package_type = models.CharField(choices=ITEMS, max_length=50)
    gender = models.CharField(choices=GENDER, max_length=50)

    def __unicode__(self):
        return self.email
