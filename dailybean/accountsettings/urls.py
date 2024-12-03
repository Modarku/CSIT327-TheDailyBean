from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_view, name='account'),
    path('set-default-address/<int:address_id>/', views.set_default_address, name='set_default_address'),
    path('get-address/<int:address_id>/', views.get_address, name='get_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('cancel-subscription/<int:subscription_id>/', views.cancel_subscription, name='cancel_subscription'),
]