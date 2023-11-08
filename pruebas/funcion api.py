import requests
estado = "Valparaiso" #variable que tiene que ingresar el usuario region
ciudad = "Valparaiso" #variable que tiene que ingresar el usuario comuna
url = ["http://api.airvisual.com/v2/city?city="+ciudad+"&state="+estado+"&country=Chile&key=4217e686-4099-4071-b670-5664769faaad"]
url = "".join(url)
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
alo = response.json()
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