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

    def buscar_filho(self, no, letra):
        for filho in no.filhos:
            if filho.char == letra:
                return filho
        return None

# -------------------------------------------------------------------------------------------
# trocar append por insert na posicao certa -> deixa os filhos em ordem alfabetica (buscar_prefixo ja sai ordenado)

    def inserir(self, palavra, valor): # nome, corpo celeste
        atual = self.raiz
        # adiciona cada letra que ainda nao existe -> se exister apenas passa por ela
        for l in palavra:
            filho = self.buscar_filho(atual, l)
    
            if filho is None:
                filho = NoTrie(l)
                atual.filhos.append(filho) 
                
            atual = filho        
        # marca o fim e aponta para o corpo celeste
        atual.fim = True
        atual.valor = valor
        
    def buscar(self, palavra):
        atual = self.raiz

        for l in palavra:
            filho = self.buscar_filho(atual, l)
            if filho is None:
                return None
            atual = filho
        
        if atual.fim:
            return atual.valor
        
        return None

    def buscar_prefixo(self, prefixo):
        pass
    def remover(self, palavra): 
        pass
    def nos_visitados(self):
        pass