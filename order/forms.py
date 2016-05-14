from django import forms
from django.forms import ModelForm
from .models import *


class OrderForm(ModelForm):
    dropoff_addr = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'},), label='Drop off Address')
    dropoff_time = forms.DateTimeField(input_formats=["%Y-%m-%d %I:%M %p",], widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'},), label='Drop off Time', error_messages={'invalid':'Drop off Time should be in format \'2016-05-03 05:53 PM\''})
    class Meta:
        model = Order
        fields = ['dropoff_addr', 'dropoff_time']
