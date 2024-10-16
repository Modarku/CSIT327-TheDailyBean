from django import forms
from home.models import Product
from django.core.exceptions import ValidationError

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'imageurl', 'description', 'total_rating']

class ModifyProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'imageurl', 'description']

