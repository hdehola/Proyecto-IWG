from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from urllib.error import HTTPError
import urllib.request
import requests
import json
import os
from django.conf import settings

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
    return render(request,'corazon.html',{ })#hacer el html que contenga la idea corazon

def estados(request, imageName):
    estado = imageName
    if estado == "Arica":
        estado = "Arica y Parinacota"
    if estado == "OHiggins":
        estado = "O'Higgins"
    if estado == "lagos":
        estado = "Los Lagos"
    if estado == "rios":
        estado = "Los Rios"
    if estado == "metropo":
        estado = "Santiago Metropolitan"
    url = "http://api.airvisual.com/v2/cities?state="+estado+"&country=Chile&key=4217e686-4099-4071-b670-5664769faaad"
    
    try:
        response = requests.get(url)
        alo = response.json()
        if alo["status"] == "success":
            cities = [data["city"] for data in alo.get("data", [])]
        else:
            cities = ["Zona no disponible"]
            print(estado)
    except requests.exceptions.RequestException as e:
        cities = ["Error en la solicitud:", str(e)]
    return JsonResponse({'cities': cities})

def ciudad_nombre(city_name):
    print("Nombre de la ciudad:", city_name)

    return HttpResponse("Recibido: " + city_name)

def obtener_calidad_aire_ciudad(request, imageName, boton):
    estado = str(imageName)
    ciudad = str(boton)
    url = "http://api.airvisual.com/v2/city?city="+ciudad+"&state="+estado+"&country=Chile&key=4217e686-4099-4071-b670-5664769faaad"
    try:
        response = requests.get(url)
        alo = response.json()
        if alo["status"] == "success":
            dato = alo["data"]["current"]["pollution"]["aqius"]

            if 0 <= dato <= 50:
                calidad_aire = "Buena"
                texto = "La calidad del aire se considera satisfactoria y la contaminación atmosferica presenta un riesgo escaso o nulo."
            elif 50 < dato <= 100:
                calidad_aire = "Moderada"
                texto = "La calidad del aire se es aceptable pero podria existir una preocupación hacia un grupo muy pequeño de personas altamente sensible a la contaminacion atmosferica."
            elif 100 < dato <= 150:
                calidad_aire = "Perjudicial"
                texto = "La calidad del aire puede presentar cierto riesgo para los grupos de personas sensibles o con  dificultades respiratorias. Probablemente la población general no se vea afectada."
            elif 150 < dato <= 200:
                calidad_aire = "Insalubre"
                texto = "La calidad del aire no es optima. Todos puedes comenzar a peder efdectos menores en su salud y los grupos mas sensibles pueden padecer efectos graves."
            elif 200 < dato <= 300:
                calidad_aire = "Riesgoso"
                texto = "Advertencia sanitaria. Es mayor la probabilidad de que la poblacion general se vea afectada."
            else:
                calidad_aire = "Peligroso"
                texto = "Alerta sanitaria. La poblacion general puede padecer graves efectos en su salud."

            return JsonResponse({'dato': dato, 'comuna': ciudad, 'texto': texto})
        else:
            return JsonResponse({'error': 'Error en la respuesta de la API'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error en la solicitud: {str(e)}'})

def api(request):
    try:
        ruta=os.path.join(settings.BASE_DIR,"tasks","geografia.json")
        if request.method == 'POST':
            ciudad = request.POST["ciudad"]
            with open(ruta, 'r', encoding='utf-8') as archivo_json:  
                lista_de_diccionarios = json.load(archivo_json)
            for diccionario in lista_de_diccionarios:
                if diccionario["Comuna"] == ciudad:
                    estado = diccionario["Región"]
            if ciudad=="Llay-Llay":
                ciudad="Llaillay"
            ciudad =ciudad.replace(' ', '%20').replace('\xa0', '').replace("\xf3", 'o').replace("\xed", 'i').replace('\xe9', 'e').replace("\xf1", 'n').replace("\xe1", 'a').replace('\xc1','A')
            estado = estado.replace(' ', '%20').replace('\xa0', '').replace('\xed', 'i').replace('\xe1','a').replace("\xf3", 'o').replace("\xd1", 'N')
            url_2= ('https://api.tomorrow.io/v4/weather/realtime?location='+estado,' ',ciudad+'&apikey=cRvA0jgpepZ88dCz8vK5S8HrcL5qPm8C')
            url_2 = "".join(url_2)
            payload={}
            headers = {}
            response = requests.request("GET", url_2, headers=headers, data=payload)
            ola= response.json()
            ciudad=ciudad.replace('%20',' ')
            estado=estado.replace('%20',' ')
            if ciudad=="Llaillay":
                ciudad="Llay-Llay"
            if len(ola) == 2:
                dato = {'humedad': str(ola['data']['values']['humidity'])+'%',
                        'Probabilidad_de_Lluvia': str(ola["data"]["values"]["precipitationProbability"])+'%',
                        'Velocidad_del_Viento': str(ola["data"]["values"]["windSpeed"])+'[Km/h]',
                        'Dirección_del_Viento': str(ola["data"]["values"]["windDirection"]),
                        'Temperatura': str(ola["data"]["values"]["temperature"])+'°C',
                        'Sensación_Térmica': str(ola["data"]["values"]["temperatureApparent"])+'°C',
                        'Comuna': str(ciudad),
                        'Región': str(estado)
                        }
                return render(request,'api_v.html', dato)
    except HTTPError as e:
        if e.code == 404:
            return render(request, "error.html")
        
def api_2(request):
    estado2 = "Los lagos" #variable que tiene que ingresar el usuario region
    estado2 = estado2.replace(' ', '%20')
    ciudad2 = "Osorno" #variable que tiene que ingresar el usuario comuna
    ciudad2 = ciudad2.replace(' ', '%20')
    url_2= ('https://api.tomorrow.io/v4/weather/realtime?location='+estado2,' ',ciudad2+'&apikey=cRvA0jgpepZ88dCz8vK5S8HrcL5qPm8C')
    url_2 = "".join(url_2)
    payload={}
    headers = {}
    response = requests.request("GET", url_2, headers=headers, data=payload)
    ola= response.json()
    if len(ola) == 2:
        valores= {
            'humedad': str(ola['data']['values']['humidity'])+'%',
            'Probabilidad_de_Lluvia': str(ola["data"]["values"]["precipitationProbability"])+'%',
            'Velocidad_del_Viento': str(ola["data"]["values"]["windSpeed"])+'[Km/h]',
            'Dirección_del_Viento': str(ola["data"]["values"]["windDirection"]),
            'Temperatura': str(ola["data"]["values"]["temperature"])+'°C',
            'Sensación_Térmica': str(ola["data"]["values"]["temperatureApparent"])+'°C'
            }
        return render(request,'api_v_2.html', valores)
    else:
        print("API en cooldown")
        
def prueba(request):        
    return render(request, 'prueba.html',{})