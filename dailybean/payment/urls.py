from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
]