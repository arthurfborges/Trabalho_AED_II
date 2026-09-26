# cria um arquivo json com todos os "bodies" da API - usado como reserva caso nao consiga acesso a API

import json
import os
import requests

URL = "https://api.le-systeme-solaire.net/rest/bodies"


def baixar_corpos():
    token = os.environ["SOLAR_API_KEY"]
    headers = {"Authorization": "Bearer " + token}

    resposta = requests.get(URL, headers=headers, timeout=30)
    resposta.raise_for_status()

    return resposta.json()["bodies"]


if __name__ == "__main__":
    corpos = baixar_corpos()
    print("Quantidade de corpos:", len(corpos))

    with open("bodies.json", "w", encoding="utf-8") as f:
        json.dump(corpos, f, ensure_ascii=False, indent=2)

    print(corpos[0])