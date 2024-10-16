from django.shortcuts import render, get_object_or_404
from home.models import Product

# Create your views here.

def view_products(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
    }
    return render(request, 'products.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})