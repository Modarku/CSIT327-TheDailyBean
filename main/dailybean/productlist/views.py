from django.shortcuts import render, get_object_or_404
from .models import Product, Review
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def homepage(request):
    products = Product.objects.all()
    return render(request, 'home.html' , {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html' , {'products': products})


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    return render(request, 'post_details.html', {'product': product, 'reviews': reviews})

