import hashlib, datetime, random
import requests
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from twilio.rest import TwilioRestClient 

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework import permissions

from .permissions import IsOwnerOnly
from .serializers import OrderSerializer
from sender.models import *
from .models import *
from .forms import *


class OrderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly,)

    def perform_create(self, serializer):
		sender = Sender.objects.get(email=self.request.user)
		pickup_addr = self.request.POST.get('pickup_addr') or sender.address
		items = self.request.POST.get('items') or sender.package_type

		salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
		key = hashlib.sha1(salt+self.request.POST.get('phone')).hexdigest()

		order = serializer.save(owner=self.request.user, pickup_addr=pickup_addr, items=items, key=key)
		# send SMS to confirm 
		send_SMS(order)

		print "Please provide your address and confirm your order. http://api.pick.sam/order_confirm/%d/%s" % (order.id, order.key)

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)


def confirm_order(request, id, key):
	try:
		order = Order.objects.get(id=id, key=key)
	
		if request.method == 'POST':
			if request.POST.get('dropoff_addr'):
				order.dropoff_addr=request.POST.get('dropoff_addr')
				order.save()				
				# send delivery request api
				send_delivery_request(order)

		order.phone = order.owner.phone		
		context = {
			'id': id,
			'key': key,
			'orderform': OrderForm(initial=model_to_dict(order)),
		}

		return render(request, 'confirm_order.html', context)		
	except ObjectDoesNotExist:
		return HttpResponse('Your link is invalid or expired!')	


def order_completed(request):
	'''
	web hook for order finish
	'''
	print 'Order is successfully finished'
	print request.json()


def send_SMS(order):
	'''
	send SMS to the customer to confirm the order using twilio
	'''
	client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) 
	 
	client.messages.create(
		to=order.phone, 
		from_="+12025688404", 
		body="Please provide your address and confirm your order. http://api.pick.sa/order_confirm/%d/%s" % (order.id, order.key),  
	)


def send_delivery_request(order):
	url = 'https://app.getswift.co/api/v2/deliveries'
	header = {"Content-Type": "application/json"}
	sender = Sender.objects.get(email=order.owner)

	body = {
		"apiKey": settings.APIKEY_GETSWIFT,
		"booking":{
			"pickupDetail": {
				"name": sender.first_name + ' ' + sender.last_name,
				"phone": sender.phone,
				"address": order.pickup_addr
			},
			"dropoffDetail": {
				"name": order.contact_name,
				"phone": order.phone,
				"address": order.dropoff_addr
			}
		}
	}            

	res = requests.post(url=url, headers=header, data=json.dumps(body))
	print res.json(), '@@@@@@@@@@'		
