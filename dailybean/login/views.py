from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import LoginForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=identifier)
                except User.DoesNotExist:
                    user = None

            if user and user.check_password(password):
                auth.login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})