import requests
estado = "Valparaiso" #variable que tiene que ingresar el usuario
ciudad = "Valparaiso" #variable que tiene que ingresar el usuario
url = ["http://api.airvisual.com/v2/city?city=", ciudad, "&state=", estado, "&country=Chile&key=4217e686-4099-4071-b670-5664769faaad"]
url = "".join(url)
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
alo = response.json()
if alo ["status"] == "success":
    dato = alo["data"]["current"]["pollution"]["aqius"]
    print(dato)
else:
    print("Zona no encontrada")