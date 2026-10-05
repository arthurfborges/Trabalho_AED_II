from estruturas.tabela_hash import tabelahash
from aquisicao.api_solar import baixar_corpos
from modelos.corpoceleste import CorpoCeleste
import json

with open("aquisicao/bodies.json", encoding="utf-8") as f:
    corpos = json.load(f)

exemplo = CorpoCeleste.from_api(corpos[0])
print(exemplo.nome, exemplo.massa, exemplo.tipo)