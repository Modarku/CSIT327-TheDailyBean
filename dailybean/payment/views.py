from django.shortcuts import render, redirect
from .models import Order
from accountsettings.models import Address
from home.models import ProductSubscription, Product
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

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
    data = serializers.serialize('json', subscriptions)

    addresses = Address.objects.filter(user=request.user)
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'addresses': addresses,
        'subscriptions' : subscriptions,
        'data' : data,
    }

    return render(request, 'payment.html', context)

def confirm_payment(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('order_ids') 
        try:
            orders = Order.objects.filter(id__in=order_ids, user=request.user, date_paid__isnull=True)
            product_stock_subtract(orders)

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
            if not subscriptions:   # Handles if productsubscription is deleted
                raise Exception("Payment expired, try again.")
            subscription_stock_subtract(subscriptions)
            current_time = timezone.now()
            new_next_monthly = current_time + relativedelta(months=+1)
            subscriptions.update(next_monthly=new_next_monthly)
            subscriptions.update(is_active=True)

            return redirect('success') 
        except Exception as e:
            print(f"An error occurred while processing your payment. {str(e)}")
            return redirect('subscription_payment')   
        
@csrf_exempt
def delete_subscription(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            subscriptions = json.loads(data)
            for subscription in subscriptions:
                for key in subscription:
                    if(key == 'pk'):
                        print(subscription[key])
                        ProductSubscription.objects.filter(id=subscription[key]).delete()

            return JsonResponse({"status": "success"})
        return JsonResponse({"status" : "error"}, status=400)
    except Exception as e:
        print(f"Error {e}")
            
def success_view(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
    }

    return render(request, 'success.html', context)

def product_stock_subtract(orders):
    for order in orders:
        product = Product.objects.get(id=order.product.id)
        product.stock -= order.product_amount
        product.save()
        # print(product.stock + 1)
        # print(order.product_amount)
        # print(product.stock + 1 - order.product_amount)

def subscription_stock_subtract(subscriptions):
    for subscription in subscriptions:
        product = Product.objects.get(id=subscription.product.id)
        product.stock -= 1
        product.save()