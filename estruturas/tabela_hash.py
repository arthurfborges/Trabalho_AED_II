# "valor" é genérico; no sistema, guarda objetos CorpoCeleste (chave = nome em minúsculo)

def hash_function(str_hash):
    acum = 0
    for c in str_hash:
        acum = (acum * 31 + ord(c))
    return acum

class No:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor 
        self.prox = None
        self.id_hash = 0

class tabelahash:
    def __init__(self, tam = 16):
        self.buckets = [None] * tam # encadeamento
        self.n = 0
        self.tam = tam
        self.colisoes = 0
        self.rehashes = 0

    def load_factor(self):
        return self.n/ self.tam

    def inserir(self, chave, valor):
        h = hash_function(chave)
        pos = h % self.tam
        atual = self.buckets[pos]

        while atual is not None: # percorre a lista substituindo os conteudos antigos, caso ocorra uma inserção com a mesma chave
            if atual.chave == chave:
                atual.valor = valor
                return
            atual = atual.prox

        if self.buckets[pos] is not None: # colisao
            self.colisoes += 1

        novo = No(chave, valor)
        novo.id_hash = h
        novo.prox = self.buckets[pos]
        self.buckets[pos] = novo
        self.n += 1

        if self.load_factor() >= 0.75:
            self._rehash()

    def buscar(self, chave):
        pos = hash_function(chave) % self.tam
        atual = self.buckets[pos]

        while atual is not None and atual.chave != chave:
            atual = atual.prox

        return atual

    def remover(self, chave):
        pos = hash_function(chave) % self.tam
        atual = self.buckets[pos]

        ant = None
        while atual is not None and atual.chave != chave:
            ant = atual
            atual = atual.prox

        if atual is None: 
            return # nao encontrou
        
        # deleta o no "atual" = chave
        if ant is None:
            self.buckets[pos] = atual.prox
        else:
            ant.prox = atual.prox 

        self.n -= 1
        return
        
    def _rehash(self):
        antigo = self.buckets
        self.tam *= 2
        self.buckets = [None] * self.tam
        self.rehashes += 1

        for cabeca in antigo:
            atual = cabeca
            while atual is not None:
                prox = atual.prox
                i = atual.id_hash % self.tam

                if self.buckets[i] is not None: # conta as colisoes do rehash - infla o numero mas gera uma metrica mais precisa
                    self.colisoes += 1

                atual.prox = self.buckets[i] # faz a ligcao ao no do novo hashmap
                self.buckets[i] = atual
                atual = prox    

    def valores(self):
        # percorre todos os buckets (usado em listagens e filtros)
        for cabeca in self.buckets:
            atual = cabeca
            while atual is not None:
                yield atual.valor
                atual = atual.prox