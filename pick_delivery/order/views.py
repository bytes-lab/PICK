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

from sender.models import *
from .models import *
from .forms import *

# put your twilio credentials here 
ACCOUNT_SID = "AC20c84dff711e30719413dd2cd9d7469b" 
AUTH_TOKEN = "7c41ee1f56e84bd3bb4ecf549cbe6eaf" 

APIKEY_GETSWIFT = "622a6564-6c73-4350-94f5-072a406fd4b7"


@login_required
def new_order(request):
	if request.method == 'GET':		
		sender = Sender.objects.get(email=request.user)

		# input extra input for a new sender
		if sender.phone == None:
			return HttpResponseRedirect('/register_sender/')

		form = OrderForm(initial={'pickup_addr': sender.address })
	else:
		form = OrderForm(request.POST)
		if form.is_valid():			
			post = form.save(commit=False)			
			post.owner = request.user

			# generate security key
			salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
			post.key = hashlib.sha1(salt+str(post.phone)).hexdigest()
			post.status = 0
			post.save()

			# send SMS to confirm 
			client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
			 
			# client.messages.create(
			# 	to=post.phone, 
			# 	from_="+12025688404", 
			# 	body="Please provide your address and confirm your order. http://api.pick.sa/order_confirm/%d/%s" % (post.id, post.key),  
			# )
			print "Please provide your address and confirm your order. http://api.pick.sam/order_confirm/%d/%s" % (post.id, post.key), "#########3"
			return HttpResponseRedirect('/')

	context = {
		'orderform': form,
	}
	return render(request, 'orders.html', context)

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

# web hook for order finish
def order_completed(request):
	print 'Order is successfully finished'
	print request.json()

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

	print body, '##################'
	res = requests.post(url=url, headers=header, data=json.dumps(body))

	print res.json()		

