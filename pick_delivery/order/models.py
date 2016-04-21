from __future__ import unicode_literals

from django.db import models
from django.conf import settings


ITEMS = (
    (0, 'Food'),
    (1, 'Electironics'),
    (2, 'Leather'),
    (3, 'Machinery'),
    (4, 'Utility'),
    (5, 'Household')
)

PAYMENT_TYPE = (
	(0, 'COD'),
	(1, 'Pre-paid'),
)

STATUS = (
	(0, 'Started'),
	(1, 'Published'),
	(2, 'Finished'),
)


class Order(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	pickup_addr = models.CharField(max_length=250)
	dropoff_addr = models.CharField(max_length=250, blank=True, null=True)
	contact_name = models.CharField(max_length=250)
	phone = models.CharField(max_length=20)
	pickup_time = models.DateTimeField()
	dropoff_time = models.DateTimeField()
	items = models.IntegerField(choices=ITEMS)
	payment_type = models.IntegerField(choices=PAYMENT_TYPE)
	key = models.CharField(max_length=100)
	status = models.IntegerField(choices=STATUS, default=0)

	def __str__(self):
		return self.contact_name
