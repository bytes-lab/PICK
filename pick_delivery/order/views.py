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
from twilio.rest import TwilioRestClient 

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import OrderSerializer
from sender.models import *
from .models import *
from .forms import *

# put your twilio credentials here 
ACCOUNT_SID = "AC20c84dff711e30719413dd2cd9d7469b" 
AUTH_TOKEN = "7c41ee1f56e84bd3bb4ecf549cbe6eaf" 

APIKEY_GETSWIFT = "622a6564-6c73-4350-94f5-072a406fd4b7"


@api_view(['GET', 'POST'])
def order_list(request):
	"""
	List all orders, or create a new order.
	"""
	if request.method == 'GET':
		sender = Sender.objects.get(email=request.user)

		# input extra input for a new sender
		if sender.phone == None:
			return HttpResponseRedirect('/register_sender/')

		orders = Order.objects.all()
		serializer = OrderSerializer(orders, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = OrderSerializer(data=request.data)
		if serializer.is_valid():
			serializer.owner = request.user

			# generate security key
			salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
			serializer.key = hashlib.sha1(salt+str(serializer.phone)).hexdigest()
			serializer.status = 0
			serializer.save()

			# send SMS to confirm 
			send_SMS(serializer)

			print "Please provide your address and confirm your order. http://api.pick.sam/order_confirm/%d/%s" % (serializer.id, serializer.key), "#########3"

			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def confirm_order(request, id, key):
	try:
		order = Order.objects.get(id=id, key=key)
	
		error_msg = ''
		if request.method == 'POST':
			if request.POST.get('dropoff_addr'):
				order.dropoff_addr=request.POST.get('dropoff_addr')
				order.save()
				
				# send delivery request api
				send_delivery_request(order)
			else:
				error_msg = "You should provide a valid drop off address!"

		context = {
			'id': id,
			'key': key,
			'orderform': OrderForm(initial=model_to_dict(order)),
			'error_msg': error_msg,
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
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
		to=order.phone, 
		from_="+12025688404", 
		body="Please provide your address and confirm your order. http://api.pick.sa/order_confirm/%d/%s" % (order.id, order.key),  
	)


def send_delivery_request(order):
	url = 'https://app.getswift.co/api/v2/quotes'
	header = {"Content-Type": "application/json"}
	sender = Sender.objects.get(email=order.owner)

	body = {
		"apiKey": APIKEY_GETSWIFT,
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
	# print res.json()		
