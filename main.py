from estruturas.tabela_hash import tabelahash
from aquisicao.api_solar import baixar_corpos
from modelos.corpoceleste import CorpoCeleste
import json

with open("aquisicao/bodies.json", encoding="utf-8") as f:
    corpos = json.load(f)

tabela = tabelahash()
for d in corpos:
    c = CorpoCeleste.from_api(d)
    tabela.inserir(c.nome.lower(), c)

print("Corpos no JSON:", len(corpos))
print("Corpos na hash:", tabela.n)
print("Tamanho:", tabela.tam)
print("Rehashes:", tabela.rehashes)
print("Colisões:", tabela.colisoes)
print("Load factor:", tabela.load_factor())
