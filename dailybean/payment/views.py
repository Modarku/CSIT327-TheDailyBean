from django.shortcuts import render, redirect
from .models import Order
from accountsettings.models import Address
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.db import models


# Create your views here.

from django.conf import settings

def payment_view(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('checkout-box') 
        orders = Order.objects.filter(id__in=order_ids)

        addresses = Address.objects.filter(user=request.user)
        context = {
            'is_authenticated': request.user.is_authenticated,
            'is_admin': request.user.is_staff,
            'addresses': addresses,
            'orders' : orders,
        }

        return render(request, 'payment.html', context)
    else:
        return redirect('cartpage')
    
def confirm_payment(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('order_ids') 
        try:
            orders = Order.objects.filter(id__in=order_ids, user=request.user, date_paid__isnull=True)
            orders.update(date_paid=timezone.now()) 
            return redirect('success') 
        except Exception as e:
            messages.error(request, "An error occurred while processing your payment.")
            return redirect('payment')  
        
def success_view(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
    }

    return render(request, 'success.html', context)

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    card_holder = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)  # Store last 4 digits only
    expiry_date = models.DateField()
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} for Order {self.order.id}"
