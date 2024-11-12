from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import Product
from payment.models import Order

# Create your views here.

def view_products(request):
    page = request.GET.get('page', 'products')

    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
    }
    return render(request, 'products.html', context)

def product_detail(request, id):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'product': get_object_or_404(Product, id=id),
    }
    return render(request, 'product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    quantity = int(request.POST.get('quantity', 1))

    total_price = product.price * quantity

    Order.objects.create(
        product=product,
        user=user,
        product_amount=quantity,
        total=total_price,
        date_paid=None
    )

    return redirect('product_list')