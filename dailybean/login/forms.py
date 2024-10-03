from django import forms
from .models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    identifier = forms.CharField(label='Username or Email', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("Passwords do not match")
        
        return password_confirm