from django.shortcuts import render
from home.models import Product

# Create your views here.

def view_products(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
    }
    return render(request, 'products.html', context)