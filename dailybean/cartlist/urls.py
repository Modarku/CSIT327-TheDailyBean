from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='cartpage'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('update-order-quantity/', views.update_order_quantity, name='update_order_quantity'),
]
