from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from .models import *


@login_required
def register_sender(request):
	sender = Sender.objects.get(email=request.user)
	if request.method == 'GET':
		form = SenderForm(initial=model_to_dict(sender))
	else:
		form = SenderForm(request.POST)
		if form.is_valid():			
			post = form.save(commit=False)			
			post.id = sender.id
			post.password = sender.password
			post.username = sender.username
			# post.is_staff = sender.is_staff
			post.save()
			return HttpResponseRedirect('/orders/')

	context = {
		'senderform': form,
		'id':id,
	}

	return render(request, 'register_sender.html', context)
