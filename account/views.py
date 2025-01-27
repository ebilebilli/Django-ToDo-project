from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def register_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passowrds do not matches')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used ')  
        else:
            User.objects.create_user(username, email, password1)
        messages.success('Account created')
        return redirect('account:login')
    
    return render(request, 'account:register')


def logout_request(request):
    return redirect('index')