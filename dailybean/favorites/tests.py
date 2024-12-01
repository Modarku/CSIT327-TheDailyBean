from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_favorites, name='user_favorites'),
    path('toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
]