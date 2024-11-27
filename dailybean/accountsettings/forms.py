# forms.py
from django import forms
from login.models import User
from .models import Address
from django.contrib.auth.forms import SetPasswordForm 

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'name', 'street_number', 'street', 'city', 'state', 'country', 'additional_details'
        ]