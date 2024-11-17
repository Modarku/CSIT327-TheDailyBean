from django.shortcuts import render
from .models import Favorite

# Create your views here.
def get_favorites_user(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'user_favorites': Favorite.objects.filter(user=user_instance),
    }
    return render(request, 'user_fav.html', context)

def get_favorites_product(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'product_favorites': Favorite.objects.filter(product=product_instance),
    }
    return render(request, 'user_fav.html', context)

