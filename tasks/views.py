from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

def Home(request):
    return render(request, 'Home.html')

def wenapo(request):

    if request.method == 'GET':         
        return render(request, 'signup.html',
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
