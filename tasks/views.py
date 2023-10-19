from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

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
                return HttpResponse('User created succesfully')
            except:
                return HttpResponse('Username already exists')
        return HttpResponse('Password do not match')
def login(request):
    return render(request, 'login.html')#{'form': User} buscar si es que existe un formulario para login precreado por django

def nosotros(request):
    return render(request,'about-us.html')#hacer el html que contenga la informacion sobre nosotros

def corazon(request):
    return render(request,'corazon.html')#hacer el html que contenga la idea corazon