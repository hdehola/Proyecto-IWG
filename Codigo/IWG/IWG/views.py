from django.http import HttpResponse
from django.template import Template, Context

def home(Request):
    docu_externo = open("C:/Users/gonza/OneDrive/Escritorio/Uni/1°año/2° semestre/IWG/Proyecto-IWG-1/IWG/IWG/Plantillas/Diseño.html")
    planti = Template(docu_externo.read())
    docu_externo.close()
    ctx = Context()
    docu = planti.render(ctx)
    return HttpResponse(docu)

def alo(request):
    return HttpResponse("saludos")
