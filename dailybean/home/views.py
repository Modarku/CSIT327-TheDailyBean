from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout

def homepage(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all().order_by('-rating')[:3],
    }
    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('homepage')

