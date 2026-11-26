from estruturas.interfaces import TrieInterface

class NoTrie:
    def __init__(self, char):
        self.char = char
        self.filhos = []      # lista de NoTrie, ordenada por char
        self.fim = False      # marca fim de um nome
        self.valor = None     # CorpoCeleste quando fim=True

class Trie(TrieInterface):
    def __init__(self):
        self.raiz = NoTrie(None) # raiz nao precisa de letra
        self.visitados = 0

    def buscar_filho(self, no, letra):
        for filho in no.filhos:
            if filho.char == letra:
                return filho
        return None

# -------------------------------------------------------------------------------------------
# trocar append por insert na posicao certa -> deixa os filhos em ordem alfabetica (buscar_prefixo ja sai ordenado)

    def inserir(self, palavra, valor): # nome, corpo celeste
        self.visitados = 0
        atual = self.raiz
        # adiciona cada letra que ainda nao existe -> se exister apenas passa por ela
        for l in palavra:
            filho = self.buscar_filho(atual, l)
    
            if filho is None:
                filho = NoTrie(l)
                atual.filhos.append(filho) 
                
            atual = filho      
            self.visitados += 1  
        # marca o fim e aponta para o corpo celeste
        atual.fim = True
        atual.valor = valor

    def buscar(self, palavra):
        self.visitados = 0
        atual = self.raiz

        for l in palavra:
            filho = self.buscar_filho(atual, l)
            if filho is None:
                return None
            atual = filho
            self.visitados += 1
        
        if atual.fim:
            return atual.valor
        
        return None

    def rec_prefixos(self, no, palavras):
        self.visitados += 1
        if no.fim:
            palavras.append(no.valor)
        
        for filho in no.filhos:
            self.rec_prefixos(filho, palavras)

    def buscar_prefixo(self, prefixo):
        self.visitados = 0
        atual = self.raiz
        palavras = []

        for l in prefixo: # pula todo o prefixo
            filho = self.buscar_filho(atual, l)
            if filho is None:
                return []
            atual = filho
            self.visitados += 1

        self.visitados -= 1 # o rec_prefixos conta o atual de novo, entao tira 1 pra nao contar duplicado
        self.rec_prefixos(atual, palavras)
        return palavras

    def remover(self, palavra):
        self.visitados = 0
        atual = self.raiz
        caminho = []

        for l in palavra: # pula todo o prefixo
            filho = self.buscar_filho(atual, l)
            if filho is None:
                return False
            caminho.append((atual, filho))
            atual = filho
            self.visitados += 1

        if atual.fim:
            atual.fim = False
            atual.valor = None

            for pai, no in reversed(caminho):
                if not no.fim and not no.filhos:
                    pai.filhos.remove(no)
                else:
                    break
            return True
        return False

    def nos_visitados(self):
        return self.visitados