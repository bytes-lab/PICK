from django import forms
from sender.models import *
from order.models import ITEMS

class SenderForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True, 'readonly':True, 'class': 'form-control'}), label="Email Address")
    phone = forms.RegexField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}), regex=r'^\d{9,15}$', 
        error_messages = {'invalid': "Phone number must be entered in the format: '999999999'. Up to 15 digits allowed."}, label="Phone Number")

    class Meta:
        model = Sender
        fields = ['first_name', 'last_name', 'gender', 'email', 'address', 'store_url', 'package_type'
            , 'phone']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'address': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'store_url': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'package_type': forms.Select(
                choices=ITEMS, 
                attrs={'required': True, 'class': 'form-control'}
            ),
            'gender': forms.Select(
                choices=GENDER, 
                attrs={'required': True, 'class': 'form-control'}
            ),        
        }
        labels = {
            'address': 'Default Location',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
