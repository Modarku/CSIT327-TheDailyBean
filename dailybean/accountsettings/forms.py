# forms.py
from django import forms
from login.models import User
from django.contrib.auth.forms import SetPasswordForm 

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ChangePasswordForm(SetPasswordForm):
    pass