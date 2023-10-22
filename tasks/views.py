from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import IntegrityError

# Create your views here.

def Home(request):
    return render(request, 'Home.html')

def register(request):
    if request.method == 'GET':         
        return render(request, 'register.html',
         {'form' : UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'register.html',
                    {'form' : UserCreationForm, 
                     "error" : "El usuario ya existe"})
        return render(request, 'register.html',
                    {'form' : UserCreationForm, 
                     "error" : 'Las contraseñas no coinciden'})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def login_view(request):
    return render(request, 'login.html')#{'form': User} buscar si es que existe un formulario para login precreado por django

def nosotros(request):
    return render(request,'about-us.html')#hacer el html que contenga la informacion sobre nosotros

def corazon(request):
    return render(request,'corazon.html')#hacer el html que contenga la idea corazon

