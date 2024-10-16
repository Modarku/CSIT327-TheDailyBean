from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_products, name='adminproductpage'),
    path('add/', views.add_product, name='addproduct'),
    path('modify/<int:pk>/', views.modify_product, name='modifyproduct'),
]
