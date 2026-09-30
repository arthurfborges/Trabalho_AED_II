import requests

# 6.1. Consulta de elementos
# Permitir localizar elementos do universo a partir de alguma forma de identificação.
# Exemplos:
# ● localizar um planeta; feito
# ● localizar uma nave;
# ● localizar um personagem;
# ● localizar uma espécie;
# ● localizar um corpo celeste.

token = "SOLAR_API_KEY" # é um $env
URL = "https://api.le-systeme-solaire.net/rest/bodies"
headers = {"Authorization": "Bearer " + token}

# resposta = requests.get(URL, headers=headers)
# dados = resposta.json()

# print(dados["englishName"])
# print(dados["gravity"])

def localizar_planeta(name_searched):
    name_all_low = name_searched.strip().lower()
    response = requests.get(f"{URL}/{name_all_low}") 

    if response.status_code == 200:
        planeta = response.json()
        if planeta['isPlanet']:
            print(f"Nome: {planeta['englishName']}")
            print(f"Massa: {planeta['mass']}")
            print(f"Gravidade: {planeta['gravity']} m/s²")
        else:
            print(f"{planeta['englishName']} nao é um planeta, é um {planeta['bodyType']}")
    else:
        print("404")
        return None
