from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from home.models import ProductSubscription
from payment.models import Order
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def view_cart(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
    }

    if(request.user.is_authenticated):
        orders = Order.objects.filter(user=request.user, date_paid__isnull=True).select_related('product')
        context['orders'] = orders

    return render(request, 'cart.html', context)

@require_http_methods(["DELETE"])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order.delete()
        return JsonResponse({'message': 'Order deleted successfully.'}, status=200)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

