from django.shortcuts import render, redirect
from .models import Order
from accountsettings.models import Address
from home.models import ProductSubscription
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def payment_view(request):
    try:
        if request.method == 'POST':
            order_ids = request.POST.getlist('checkout-box')
            if not order_ids:
                messages.error(request, "No orders selected for checkout.")
                return redirect('cartpage')
            
            orders = Order.objects.filter(id__in=order_ids)
            if not orders.exists():
                messages.error(request, "No valid orders found for checkout.")
                return redirect('cartpage')
            
            order_sum = sum(order.total for order in orders)

            addresses = Address.objects.filter(user=request.user)
            context = {
                'is_authenticated': request.user.is_authenticated,
                'is_admin': request.user.is_staff,
                'addresses': addresses,
                'orders' : orders,
                'order_sum' : order_sum
            }
            return render(request, 'payment.html', context)
        else:
            return redirect('cartlist')
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def subscription_payment_view(request):

    subscriptions = ProductSubscription.objects.filter(user=request.user, is_active=False)

    addresses = Address.objects.filter(user=request.user)
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'addresses': addresses,
        'subscriptions' : subscriptions,
    }

    return render(request, 'payment.html', context)

def confirm_payment(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('order_ids') 
        try:
            orders = Order.objects.filter(id__in=order_ids, user=request.user, date_paid__isnull=True)
            orders.update(date_paid=timezone.now()) 
            return redirect('success') 
        except Exception as e:
            messages.error(request, f"An error occurred while processing your payment. {str(e)}")
            return redirect('payment')

def confirm_subscription_payment(request):
    if request.method == 'POST':
        subscription_ids = request.POST.getlist('order_ids') 
        try:
            subscriptions = ProductSubscription.objects.filter(id__in=subscription_ids, user=request.user, is_active=False)
            
            current_time = timezone.now()
            new_next_monthly = current_time + relativedelta(months=+1)
            subscriptions.update(next_monthly=new_next_monthly)
            subscriptions.update(is_active=True)

            return redirect('success') 
        except Exception as e:
            print(f"An error occurred while processing your payment. {str(e)}")
            return redirect('subscription_payment')   
        
def success_view(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
    }

    return render(request, 'success.html', context)