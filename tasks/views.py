from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
import urllib.request
from urllib.error import HTTPError
import json

# Create your views here.

def test(request):
            
    return render(request, 'test.html',{})

def newhome(request):
    return render(request,'new-home.html',{})

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
                return redirect('new-home')#home
            except IntegrityError:
                return render(request, 'register.html',
                    {'form' : UserCreationForm, 
                     "error" : "El usuario ya existe"})
        return render(request, 'register.html',
                    {'form' : UserCreationForm, 
                     "error" : 'Las contraseñas no coinciden'})

def cerrar_sesion(request):
    logout(request)
    return redirect('new-home')#home

def login_view(request):
    if request.method == 'GET':         
        return render(request, 'login_view.html', {'form' : AuthenticationForm})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login_view.html', {'form' : AuthenticationForm, 'error':'El Usuario o contraseña son incorrectos'})
        else:
            login(request, user) 
            return redirect('new-home')#home  

def nosotros(request):
    return render(request,'nosotros.html')#hacer el html que contenga la informacion sobre nosotros

def corazon(request):
    #
    return render(request,'corazon.html',{ })#hacer el html que contenga la idea corazon

def api(request): 
    estado = "Los lagos" #variable que tiene que ingresar el usuario region
    estado = estado.replace(' ', '%20')
    ciudad = "Osorno" #variable que tiene que ingresar el usuario comuna
    ciudad = ciudad.replace(' ', '%20')
    url = urllib.request.Request("http://api.airvisual.com/v2/city?city="+ciudad+"&state="+estado+"&country=Chile&key=4217e686-4099-4071-b670-5664769faaad")
    source = urllib.request.urlopen(url).read()
    alo = json.loads(source)
    if alo ["status"] == "success":
        dato = { "aqiuo": str(alo["data"]["current"]["pollution"]["aqius"]).capitalize}
        return render(request,'api_v.html', dato)
    else:
        print("error")