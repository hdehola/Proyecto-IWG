"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.views import estados, obtener_calidad_aire_ciudad

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.newhome,name='new-home'),
    path('test/', views.test, name= 'test'),
    path('prueba/', views.prueba, name= 'prueba'),
    path('register/', views.register, name ='register'),
    path('logout/', views.cerrar_sesion, name= 'logout'),
    path('login/', views.login_view, name= 'login'),#url para el login
    path('about-us/',views.nosotros, name= 'nosotros'),#url para la informacion sobre nosotros 
    path('project-shake-corazon/',views.corazon,name= 'corazon'),#url para redireccionar a la idea corazon
    path('test/test',views.api,name='api'),
    path('apis/',views.api_2,name='api2'),
    path('estados/<str:imageName>/', views.estados, name='estados'),
    path('ciudad_nombre/<str:city_name>/', views.ciudad_nombre, name='ciudad nombre'),
    path('obtener_calidad_aire_ciudad/<str:imageName>/<str:boton>/', views.obtener_calidad_aire_ciudad, name='obtener_calidad_aire_ciudad'),
]