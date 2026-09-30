# "valor" deverá ser substituido pelos dados que queremos guardar sobre os corpos celestes

def hash_function(str_hash, tam):
    acum = 0
    for c in str_hash:
        acum = (acum * 31 + ord(c)) % tam

    return result

class No:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor 
        self.prox = None

class Map:
    def __init__(self, tam = 16):
        self.buckets[[None] * tam] # encadeamento
        self.n = 0
        self.colisoes = 0

    def load_factor(self):
        return self.n/ self.tam

    def inserir(self, chave, valor):
        pos = hash_function(chave)
        atual = self.buckets[pos]
        anterior = None

        while atual is not None: # percorre a lista substituindo os conteudos antigos, caso ocorra uma inserção com a mesma chave
            if atual.chave == chave:
                atual.valor = valor

            atual = atual.prox

        if self.buckets[pos] is not None: # colisao
            self.colisoes += 1

        novo = No(chave, valor)
        novo.prox = self.buckets[pos]
        self.buckets[pos] = novo
        self.n += 1

        if self.load_factor >= 0.75:
            self._rehash

    def buscar(self, chave):
        pass
    def remover(self, chave):
        pass    
    def _rehash(self):
        pass
