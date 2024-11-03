from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import UserEditForm, SetPasswordForm, AddressForm
from .models import Address
from payment.models import Order
from django.contrib import messages
from django.http import JsonResponse

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
                messages.error(request, password_form.errors, extra_tags='msg_add_address')
    else:
        form = UserEditForm(instance=user)
        password_form = SetPasswordForm(user)
        address_form = AddressForm()

    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user, date_paid__isnull=False)

    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user,
        'form': form,
        'password_form': password_form,
        'address_form': address_form,
        'addresses': addresses,
        'orders': orders,
    }

    return render(request, 'accounts.html', context)

# Address Views
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('account') 
    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
        'address': address,
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