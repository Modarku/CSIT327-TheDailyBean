from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('logout/', views.logout_view, name='logout'),
]
