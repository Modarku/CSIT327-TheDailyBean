from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import UserEditForm, SetPasswordForm, AddressForm
from .models import Address
from payment.models import Order
from home.models import ProductSubscription
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import logging

logger = logging.getLogger(__name__)

def account_view(request):
    user = request.user

    if request.method == 'POST':
        # Handle user information update
        if 'edit_user' in request.POST:
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your information has been updated.', extra_tags='msg_edit_user')
                return redirect('account')
            else:
                messages.error(request, form.errors, extra_tags='msg_edit_user') 
        else:
            form = UserEditForm(instance=user)

        # Handle password change
        if 'change_password' in request.POST:
            password_form = SetPasswordForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Your password has been changed.', extra_tags='msg_change_password')
                return redirect('login')
            else:
                messages.error(request, password_form.errors, extra_tags='msg_change_password') 
        else:
            password_form = SetPasswordForm(user)
        
        # Handle address creation
        if 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
                messages.success(request, 'Address has been added.', extra_tags='msg_add_address')
                return redirect('account')
            else:
                messages.error(request, address_form.errors, extra_tags='msg_add_address')
        else:
            address_form = AddressForm()
    else:
        form = UserEditForm(instance=user)
        password_form = SetPasswordForm(user)
        address_form = AddressForm()

    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user, date_paid__isnull=False)
    subscriptions = ProductSubscription.objects.filter(user=request.user, is_active=True)

    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user,
        'form': form,
        'password_form': password_form,
        'address_form': address_form,
        'addresses': addresses,
        'orders': orders,
        'subscriptions' : subscriptions,
    }

    return render(request, 'accounts.html', context)

# Address Views
def edit_address(request, address_id):
    user = request.user
    address = get_object_or_404(Address, id=address_id)
    form = UserEditForm(instance=user)
    password_form = SetPasswordForm(user)
    address_form = AddressForm()

    if request.method == 'POST':
        address.name = request.POST.get('name')
        address.street_number = request.POST.get('street_number')
        address.street = request.POST.get('street')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.additional_details = request.POST.get('additional_details')
        address.save()
        
        messages.success(request, 'Address updated successfully.')
        return redirect('account')
    
    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user,
        'form': form,
        'password_form': password_form,
        'address_form': address_form,
    }
    
    return render(request, 'accounts.html', context)

@csrf_exempt
def delete_address(request, address_id):
    if request.method == 'DELETE':
        try:
            address = Address.objects.get(id=address_id)
            address.delete()
            return JsonResponse({'message': 'Address deleted successfully.'}, status=200)
        except Address.DoesNotExist:
            return JsonResponse({'message': 'Address not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def set_default_address(request, address_id):
    Address.objects.all().update(is_selected=False)
    selected_address = Address.objects.get(id=address_id)
    selected_address.is_selected = True
    selected_address.save()
    return redirect('account')

def get_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    data = {
        'name': address.name,
        'street_number': address.street_number,
        'street': address.street,
        'city': address.city,
        'state': address.state,
        'country': address.country,
        'additional_details': address.additional_details,
    }
    return JsonResponse(data)

@require_http_methods(["DELETE"])
def cancel_subscription(request, subscription_id):
    try:
        subscription = ProductSubscription.objects.get(id=subscription_id)
        subscription.delete()
        return JsonResponse({'message': 'Subscription cancelled successfully.'}, status=200)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Subscription not found.'}, status=404)

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if not request.user.check_password(password):
            messages.error(request, "Incorrect password.")
            return redirect('delete_account')

        user = request.user
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home.html')

    return render(request, 'delete_account.html')