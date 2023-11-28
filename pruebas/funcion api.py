import requests
estado = "O'Higgins" #variable que tiene que ingresar el usuario region
estado = estado.replace(' ', '%20')
ciudad = "San Fernando" #variable que tiene que ingresar el usuario comuna
ciudad = ciudad.replace(' ', '%20')
url = ["http://api.airvisual.com/v2/city?city="+ciudad+"&state="+estado+"&country=Chile&key=4217e686-4099-4071-b670-5664769faaad"]
url = "".join(url)
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
alo = response.json()
if alo ["status"] == "success":   #Cambiar los print por return cuando se agregue a la función#
    dato = alo["data"]["current"]["pollution"]["aqius"]
    print(dato)
    if dato >= 0 and dato <= 50:
        print(str(dato)+":", "Verde")
    if dato > 50 and dato <= 100:
        print(str(dato)+":","Amarillo")
    if dato > 100 and dato <= 150:
        print(str(dato)+":","Naranja")
    if dato > 150 and dato <= 200:
        print(str(dato)+":","Rojo")
    if dato > 200 and dato <= 300:
        print(str(dato)+":","Morado")
    if dato > 300:
        print(str(dato)+":","Cafe")
else:
    print("Zona no encontrada")

#otros datos#
'''
if alo ["status"] == "success":
    aqius = alo["data"]["current"]["pollution"]["aqius"]
    mainus = alo["data"]["current"]["pollution"]["mainus"]
    aqicn = alo["data"]["current"]["pollution"]["aqicn"]
    maincn = alo["data"]["current"]["pollution"]["maincn"]
    print(aqius)
    print(mainus)
    print(aqicn)
    print(maincn)
else:
    print("Zona no encontrada")
'''