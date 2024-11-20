from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_products, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-subscription/', views.add_to_subscription, name='add_to_subscription'),
    path('<int:product_id>/delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('<int:product_id>/edit-review/<int:review_id>/', views.edit_review, name='edit_review'),
]
