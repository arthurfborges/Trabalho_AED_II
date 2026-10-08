# Topico 7 - planejamento da missao utilizando algoritmo guloso

# Opção A: Planejamento e Triagem de Missões (Otimização Logística)

# estratégia gulosa: seleciona candidatos pelo custo beneficio,
# respeitando um orçamento de distância total disponível para a missão,
# e utiliza os seguintes criterios de seleção:
# - corpos com mais luas (mais luas = mais objetos de estudo)
# - planetas anoes tem prioridade por serem mais raros
# - gravidade maior fornece maior facilidade para a instrumentação da pesquisa


class Candidato:
    def __init__(self, corpo, distancia, potencial_cientifico):
        self.corpo = corpo
        self.distancia = distancia
        self.potencial_cientifico = potencial_cientifico

    def razao(self):
        return self.potencial_cientifico / self.distancia


def calcular_potencial(corpo):
    score = corpo.num_luas 

    if corpo.tipo == "Dwarf Planet":
        score += 1

    score += (corpo.gravidade or 0) * 0.1

    return score

def montar_candidatos(corpos):
    candidatos = []
    for corpo in corpos:
        if corpo.dist_orbital:  #não divide por zero
            candidatos.append(
                Candidato(corpo, corpo.dist_orbital, calcular_potencial(corpo))
            )
    return candidatos

def planejar_missao(candidatos, orcamento):
    ordenados = sorted(candidatos, key=lambda c: c.razao(), reverse=True)

    selecionados = []
    custo_total = 0

    for c in ordenados:
        if custo_total + c.distancia <= orcamento:
            selecionados.append(c)
            custo_total += c.distancia

    return selecionados, custo_total

if __name__ == "__main__":
    from aquisicao.api_solar import obter_corpos
    from modelos.corpoceleste import CorpoCeleste

    corpos = [CorpoCeleste.from_api(d) for d in obter_corpos()]
    candidatos = montar_candidatos(corpos)

    orcamento = float(input("Orçamento de distância total (km): "))
    escolhidos, custo_total = planejar_missao(candidatos, orcamento)

    for c in escolhidos:
        print(f"Distancia - {c.corpo.nome}: {c.distancia:,.0f} km - razão: {c.razao():.3e}")
    print(f"Custo total: {custo_total:,.0f} km | Sobrou: {orcamento - custo_total:,.0f} km")