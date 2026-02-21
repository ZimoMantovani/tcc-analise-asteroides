import requests
import os
import pandas as pd
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

dados = []

for asteroide in asteroides_de_hoje:
    dict_asteroide = {
        'ID': asteroide['id'],
        'Nome': asteroide['name'],
        'Perigoso': asteroide['is_potentially_hazardous_asteroid']
    }
    #print(f" ID: {id_do_asteroide} | Nome: {nome_do_asteroide} | É perigoso: {eh_perigoso}")
    dados.append(dict_asteroide)

df = pd.DataFrame(dados)
df.set_index('ID', inplace=True)

print(df.to_string())