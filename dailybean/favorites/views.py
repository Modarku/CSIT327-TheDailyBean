from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from home.models import Product
from .models import Favorite
# Create your views here.

def product_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    users = Favorite.objects.filter(product=product).select_related('user')
    return render(request, 'product_favorites.html', {'product': product, 'users': users})

@login_required
def user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
    return redirect('product_detail', id=product.id)

@login_required
def toggle_favorite_favpage(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
    return redirect('user_favorites')
