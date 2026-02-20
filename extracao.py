import requests
import os
from dotenv import load_dotenv
from datetime import date

today = date.today()

load_dotenv()
API_KEY = os.getenv('API_KEY')

r = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&api_key={API_KEY}')

json = r.json()

objetos_proximos = json['near_earth_objects']
# print(type(objetos_proximos))
# print(objetos_proximos.keys())

asteroides_de_hoje = objetos_proximos[str(today)]
#print(type(asteroides_de_hoje))

print(len(asteroides_de_hoje))


for asteroide in asteroides_de_hoje:
    nome_do_asteroide = asteroide['name']
    id_do_asteroide = asteroide['id']
    
    print(f"Nome: {nome_do_asteroide} | ID: {id_do_asteroide}")
