# Topico 7 - planejamento da missao utilizando algoritmo guloso

# Opção A: Planejamento e Triagem de Missões (Otimização Logística)

# estratégia gulosa: seleciona candidatos pelo custo beneficio,
# respeitando um orçamento de distância total disponível para a missão,
# e utiliza os seguintes criterios de seleção:
# - corpos com mais luas (mais luas = mais objetos de estudo)
# - planetas anoes tem prioridade por serem mais raros
# - gravidade maior fornece maior facilidade para a instrumentação da pesquisa


class Candidato:
    def __init__(self, nome, distancia, potencial_cientifico):
        self.nome = nome
        self.distancia = distancia
        self.potencial_cientifico = potencial_cientifico

    def razao(self):
        return self.potencial_cientifico / self.distancia


def calcular_potencial(corpo):
    score = 0

    luas = corpo.get("moons") or []
    score += len(luas)

    if corpo.get("bodyType") == "DwarfPlanet":
        score += 1

    gravidade = corpo.get("gravity")
    score += gravidade * 0.1

    return score

