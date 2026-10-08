from estruturas.tabela_hash import tabelahash
from aquisicao.api_solar import obter_corpos
from modelos.corpoceleste import CorpoCeleste
from planejamento_missao_guloso import montar_candidatos, planejar_missao

def carregar():
    corpos = [CorpoCeleste.from_api(d) for d in obter_corpos()]
    tabela = tabelahash()
    for c in corpos:
        tabela.inserir(c.nome.lower(), c)
    return tabela


def metricas(t):
    print(f"Corpos na hash: {t.n} | Tamanho: {t.tam} | Rehashes: {t.rehashes}")
    print(f"Colisoes: {t.colisoes} | Load factor: {t.load_factor():.3f}")


def consultar(t):
    nome = input("Nome exato (em ingles, ex: Earth): ").strip().lower()
    no = t.buscar(nome)
    if no is None:
        print("Nao encontrado.")
        return
    c = no.valor
    print(f"{c.nome} | tipo: {c.tipo} | massa: {c.massa} kg | gravidade: {c.gravidade} m/s2")
    print(f"raio: {c.raio} km | dist. orbital: {c.dist_orbital} km | orbita: {c.ao_redor_de}")
    print(f"temp. media: {c.temp_media} K | luas: {c.num_luas}")


def pesquisar(t):
    termo = input("Trecho do nome: ").strip().lower()
    achados = [c for c in t.valores() if termo in c.nome.lower()]
    for c in sorted(achados, key=lambda c: c.nome):
        print(" -", c)
    print(f"{len(achados)} resultado(s)")


def listar(t):
    tipo = input("Tipo (Planet, Moon, Asteroid, Comet, Dwarf Planet, Star): ").strip().lower()
    g = input("Gravidade minima (enter = sem filtro): ").strip()
    gmin = float(g) if g else None
    achados = [c for c in t.valores()
               if c.tipo and c.tipo.lower() == tipo
               and (gmin is None or (c.gravidade or 0) >= gmin)]
    for c in sorted(achados, key=lambda c: c.nome):
        print(f" - {c.nome} (gravidade: {c.gravidade})")
    print(f"{len(achados)} resultado(s)")


def missao(t):
    orc = float(input("Orcamento de distancia total (km): "))
    escolhidos, custo = planejar_missao(montar_candidatos(list(t.valores())), orc)
    for c in escolhidos:
        print(f" - {c.corpo.nome}: {c.distancia:,.0f} km | potencial: {c.potencial_cientifico:.2f} | razao: {c.razao():.3e}")
    print(f"{len(escolhidos)} destinos | Custo total: {custo:,.0f} km | Sobrou: {orc - custo:,.0f} km")

def main():
    t = carregar()
    metricas(t)
    acoes = {"1": consultar, "2": pesquisar, "3": listar, "4": missao}
    while True:
        print("\n1-Consultar  2-Pesquisar por nome  3-Listar/filtrar  4-Planejar missao  5-Metricas da hash  0-Sair")
        op = input("> ").strip()
        if op == "0":
            break
        if op == "5":
            metricas(t)
        elif op in acoes:
            acoes[op](t)


if __name__ == "__main__":
    main()
