from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_favorites, name='user_favorites'),
    path('toggle_favorite/<int:product_id>/<str:redirect_url>/', views.toggle_favorite, name='toggle_favorite'),
]