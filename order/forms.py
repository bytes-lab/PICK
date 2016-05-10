from django import forms
from django.forms import ModelForm
from .models import *


class OrderForm(ModelForm):
    # pickup_time = forms.DateTimeField(input_formats=["%Y-%m-%d %I:%M %p",])

    class Meta:
        model = Order
        fields = ['dropoff_addr', 'dropoff_time']
        widgets = {
            'dropoff_addr': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'dropoff_time': forms.DateTimeInput(
                attrs={'required': True, 'class': 'form-control'},
                format='%Y-%m-%d %I:%M %p',
            ),        
        }
        labels = {
            'dropoff_addr': 'Drop off Address',
            'dropoff_time': 'Drop off Time',
        }
