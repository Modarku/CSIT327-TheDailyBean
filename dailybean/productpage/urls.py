from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_products, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
