from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from home.models import Product, Review
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def view_cart(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'cart.html', context)

