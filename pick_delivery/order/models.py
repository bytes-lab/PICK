from __future__ import unicode_literals

from django.db import models
from django.conf import settings


ITEMS = (
    ('Food', 'Food'),
    ('Electironics', 'Electironics'),
    ('Leather', 'Leather'),
    ('Machinery', 'Machinery'),
    ('Utility', 'Utility'),
    ('Household', 'Household')
)

PAYMENT_TYPE = (
	('COD', 'COD'),
	('Pre-paid', 'Pre-paid'),
)

STATUS = (
	('Initial', 'Initial'),
	('Received', 'Received'),
	('Finished', 'Finished'),
)


class Order(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders")
	pickup_addr = models.CharField(max_length=250, blank=True, null=True)
	dropoff_addr = models.CharField(max_length=250)
	contact_name = models.CharField(max_length=250)
	phone = models.CharField(max_length=20)
	pickup_time = models.DateTimeField()
	dropoff_time = models.DateTimeField()
	items = models.CharField(choices=ITEMS, null=True, max_length=50)
	payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=50)
	key = models.CharField(max_length=100)
	status = models.CharField(choices=STATUS, default='Initial', max_length=20)
	track_link = models.CharField(max_length=200, blank=True, null=True)
	
	def __str__(self):
		return self.contact_name
