import hashlib, datetime, random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.shortcuts import render

from twilio.rest import TwilioRestClient 

from .models import *
from .forms import *

# put your own credentials here 
ACCOUNT_SID = "AC20c84dff711e30719413dd2cd9d7469b" 
AUTH_TOKEN = "7c41ee1f56e84bd3bb4ecf549cbe6eaf" 

@login_required
def new_order(request):
	if request.method == 'GET':
		form = OrderForm(initial={'pickup_addr': 'Dundas St E, Toronto'})
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
			 
			client.messages.create(
				to=post.phone, 
				from_="+12025688404", 
				body="Please provide your address and confirm your order. http://api.pick.sa/order_confirm/%d/%s" % (post.id, post.key),  
			)

			return HttpResponseRedirect('/')

	context = {
		'orderform': form,
	}
	return render(request, 'orders.html', context)

