from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from home.models import Product
from .models import Favorite
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

def product_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'product': product,
        'users': Favorite.objects.filter(product=product).select_related('user')
    }
    return render(request, 'product_favorites.html', context)

@login_required
def user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'favorites': favorites.select_related('product'),
        # 'last_toggled': last_toggled
    }
    return render(request, 'favorites.html', context)

@login_required
def toggle_favorite(request, product_id, redirect_url):
    try:
        product = get_object_or_404(Product, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favorite.delete()
            messages.success(request, f'Removed {product.product_name} from your favorites.', extra_tags='red')
        else:
            messages.success(request, f'Added {product.product_name} to your favorites.', extra_tags='green')

        if redirect_url == "product_detail":
            return redirect('product_detail', id=product.id)
        else:
            # return redirect('user_favorites')
            return JsonResponse({'message': 'Success', 'status': 'ok'})
    except Exception as e:
            return JsonResponse({'message': str(e), 'status': 'error'})