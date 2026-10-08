import json
import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # sem python-dotenv, usa só as variáveis de ambiente do sistema

URL = "https://api.le-systeme-solaire.net/rest/bodies"
CAMINHO_JSON = os.path.join(os.path.dirname(__file__), "bodies.json")


def baixar_corpos():
    token = os.environ["SOLAR_API_KEY"]
    headers = {"Authorization": "Bearer " + token}

    resposta = requests.get(URL, headers=headers, timeout=30)
    resposta.raise_for_status()

    return resposta.json()["bodies"]

def salvar_corpos(corpos):
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump(corpos, f, ensure_ascii=False, indent=2)


def carregar_corpos_arquivo():
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def obter_corpos():
    try:
        corpos = baixar_corpos()
        salvar_corpos(corpos)
        print("Dados obtidos da API.")
    except (requests.RequestException, KeyError) as erro:
        print(f"Falha ao acessar a API ({erro}). Usando bodies.json local.")
        corpos = carregar_corpos_arquivo()
    return corpos


if __name__ == "__main__":
    corpos = obter_corpos()
    print("Quantidade de corpos:", len(corpos))