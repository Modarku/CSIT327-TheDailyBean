from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment'),
    path('subscribe/', views.subscription_payment_view, name='subscription_payment'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('confirm-subscription-payment/', views.confirm_subscription_payment, name='confirm_subscription_payment'),
    path('success/', views.success_view, name='success')
]