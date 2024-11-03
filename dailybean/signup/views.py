from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from login.forms import SignUpForm
from login.models import User 

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                user_modified=timezone.now(),
                user_type=User.CUSTOMER
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})