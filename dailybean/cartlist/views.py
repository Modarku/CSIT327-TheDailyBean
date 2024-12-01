from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from home.models import ProductSubscription, Product
from payment.models import Order
from django.http import HttpResponse
from django.template import loader
import json

# Create your views here.

def view_cart(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
    }

    if(request.user.is_authenticated):
        orders = Order.objects.filter(user=request.user, date_paid__isnull=True).select_related('product')
        
        #Check if product stock is available based on the order of the user
        for order in orders:
            product = Product.objects.get(id=order.product.id)
            if product.stock < order.product_amount:
               print(f'{product.product_name} currently has insufficient stock.')
               messages.error(request, f'{product.product_name} currently has insufficient stock.', extra_tags='msg_stock')

        context['orders'] = orders

    return render(request, 'cart.html', context)

@csrf_exempt
def update_order_quantity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            quantity = int(data.get('quantity'))
            total_price = float(data.get('total_price'))

            order = Order.objects.get(id=order_id)
            order.product_amount = quantity
            order.total = total_price
            order.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@require_http_methods(["DELETE"])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order.delete()
        return JsonResponse({'message': 'Order deleted successfully.'}, status=200)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

