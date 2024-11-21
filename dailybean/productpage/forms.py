from django import forms
from home.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
    
    rating = forms.FloatField(min_value=1.0, max_value=5.0)