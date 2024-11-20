from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import Product
from favorites.models import Favorite
from payment.models import Order

# Create your views here.

def view_products(request):
    page = request.GET.get('page', 'products')
    template = 'subscriptions.html' if page == 'subscriptions' else 'products.html'

    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
    }
    return render(request, template, context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    is_favorited = (
        Favorite.objects.filter(user=request.user, product=product).exists()
        if request.user.is_authenticated
        else False
    )
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'product': product,
        'favorited': Favorite.objects.filter(product=product).count(),
        'is_favorited': is_favorited,
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