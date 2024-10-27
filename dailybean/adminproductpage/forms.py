from django import forms
from home.models import Product
from django.core.exceptions import ValidationError

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_description',
            'product_ingredients',
            'product_shelflife',
            'product_image',
            'stock',
            'price'
        ]

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'product_ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'product_shelflife': forms.TextInput(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ModifyProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_description',
            'product_ingredients',
            'product_shelflife',
            'product_image',
            'stock',
            'price'
        ]

