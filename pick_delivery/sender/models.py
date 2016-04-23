from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from order.models import ITEMS

GENDER = (
	(0, 'Male'),
	(1, 'Female')
)

class Sender(AbstractUser):
    """
    Custom user class - Sender.
    """
    address = models.CharField(max_length=300)		# default location
    phone = models.CharField(max_length=50, null=True, blank=True)
    store_url = models.CharField(max_length=50)
    package_type = models.IntegerField(choices=ITEMS, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, null=True, blank=True)

    def __unicode__(self):
        return self.email
