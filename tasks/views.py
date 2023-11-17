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
    estado = imageName
    ciudad = boton
    url = f"http://api.airvisual.com/v2/city?city={ciudad}&state={estado}&country=Chile&key=4217e686-4099-4071-b670-5664769faaad"

    try:
        response = requests.get(url)
        alo = response.json()
        if alo["status"] == "success":
            dato = alo["data"]["current"]["pollution"]["aqius"]

            if 0 <= dato <= 50:
                calidad_aire = "Verde"
            elif 50 < dato <= 100:
                calidad_aire = "Amarillo"
            elif 100 < dato <= 150:
                calidad_aire = "Naranja"
            elif 150 < dato <= 200:
                calidad_aire = "Rojo"
            elif 200 < dato <= 300:
                calidad_aire = "Morado"
            else:
                calidad_aire = "Cafe"

            return JsonResponse({'dato': dato, 'calidad_aire': calidad_aire})
        else:
            return JsonResponse({'error': 'Error en la respuesta de la API'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error en la solicitud: {str(e)}'})

def api(request):
    try:
        if request.method == 'POST':
            estado = request.POST["name1"]
            estado = estado.replace(' ', '%20')
            ciudad = request.POST["name1"]
            ciudad = ciudad.replace(' ', '%20')
            url = urllib.request.Request("http://api.airvisual.com/v2/city?city="+ciudad+"&state="+estado+"&country=Chile&key=4217e686-4099-4071-b670-5664769faaad")
            url.add_header('User-Agent', "Piñera")
            source = urllib.request.urlopen(url).read()
            alo = json.loads(source)
            url_2= ('https://api.tomorrow.io/v4/weather/realtime?location='+estado,' ',ciudad+'&apikey=cRvA0jgpepZ88dCz8vK5S8HrcL5qPm8C')
            url_2 = "".join(url_2)
            url_2.add_header('User-Agent', "Piñera")
            payload={}
            headers = {}
            response = requests.request("GET", url_2, headers=headers, data=payload)
            ola= response.json()
            if alo ["status"] == "success" and len(ola) == 2:
                dato = { "aqiuo": str(alo["data"]["current"]["pollution"]["aqius"]).capitalize(),
                        'humedad': str(ola['data']['values']['humidity'])+'%',
                        'Probabilidad_de_Lluvia': str(ola["data"]["values"]["precipitationProbability"])+'%',
                        'Velocidad_del_Viento': str(ola["data"]["values"]["windSpeed"])+'[Km/h]',
                        'Dirección_del_Viento': str(ola["data"]["values"]["windDirection"]),
                        'Temperatura': str(ola["data"]["values"]["temperature"])+'°C',
                        'Sensación_Térmica': str(ola["data"]["values"]["temperatureApparent"])+'°C'
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
        