import requests
import json

url = "http://api.airvisual.com/v2/states?country=Chile&key=876c58b7-cfe7-4ce0-8cdc-c4967b660ee7"

payload={}
files={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

data = json.loads(response.text)

states = [state['state'] for state in data['data']]

state_dict = {state: [] for state in states}

#print(state_dict)
#15 ["Aisen","Antofagasta","Araucania","Arica y Parinacota","Atacama","Biobio","Coquimbo","Los Lagos","Los Rios",
# "Magallanes","Maule","O'Higgins","Santiago Metropolitan","Tarapaca","Valparaiso"]



region = "Valparaiso"  
url = f"http://api.airvisual.com/v2/cities?state={region}&country=Chile&key=876c58b7-cfe7-4ce0-8cdc-c4967b660ee7"

response = requests.get(url)
data = response.json()

comunas = []
for item in data['data']:
    comunas.append(item['city'])

#print(comunas)
# disponibles ['Concon', 'La Greda', 'La Ligua', 'Llaillay', 'Los Maitenes', 'Puchuncavi', 'Quillota', 'Quilpue',
#  'Quintero', 'San Antonio', 'San Felipe', 'Valparaiso', 'Villa Alemana', 'Vina del Mar']