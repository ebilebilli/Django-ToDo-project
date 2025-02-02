from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            messages.error(request, 'Please fill all fields')
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used')
            return render(request, 'register.html')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully')
        return redirect('account:login')
    
    return render(request, 'register.html')


def logout_request(request):
    logout(request)
    return redirect('account:login')