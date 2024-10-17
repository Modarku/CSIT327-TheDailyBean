from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, SetPasswordForm
from django.contrib import messages

def account_view(request):
    user = request.user

    if request.method == 'POST':
        # Handle user information update
        if 'edit_user' in request.POST:
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your information has been updated.', extra_tags='msg_edit_user')
                return redirect('../../account/')
            else:
                messages.error(request, form.errors, extra_tags='msg_edit_user') 

        # Handle password change
        elif 'change_password' in request.POST:
            password_form = SetPasswordForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Your password has been changed.', extra_tags='msg_change_password')
                return redirect('../../login/')
            else:
                messages.error(request, password_form.errors, extra_tags='msg_change_password') 
    else:
        form = UserEditForm(instance=user)
        password_form = SetPasswordForm(user)

    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user,
        'form': form,  # Make sure form is initialized here
        'password_form': password_form,  # Pass password form to context
    }

    return render(request, 'accounts.html', context)