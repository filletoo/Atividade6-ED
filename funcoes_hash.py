import re
import matplotlib.pyplot as plt

def carregar_nomes(arquivo, por_linha=True):
    with open(arquivo, mode='r', encoding="utf-8") as f:
        texto = f.read().lower()
        if por_linha:
            arg_r = r'[@,.;:/—!?()\n\ufeff–"]+'
        else:
            arg_r = r'[@,.;:/—!?()\n\ufeff– "]+'
            
        nomes = re.split(arg_r, texto)
        if nomes[0] == '':
            nomes = nomes[1:-1]

    return nomes

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prox = None

class HashListaLigada:
    '''Coloca pro metodo insert retornar True se for inserido 
    um novo elemento ou False se for apenas mudado o valor da
    chave'''

    '''Coloca um atributo que diz a quantidade de elementos na lista'''
    pass


class HashTable: 
    def __init__(self, M): 
        self.M = M 
        self.n = 0 
        self.table = [None] * M 

    #funcao hash discutida em sala de aula 
    def _hash(self, key): 
        h = 0
        for c in key: 
            h = (31 * h + ord(c)) % self.M 
        return h

    def hash_primeira_letra(self, key):
        return (ord(key[0]) - ord('a')) % self.M

    def hash_nativa(self, key):
        return hash(key) % self.M

    def escolher_hash(self, key, funcao):
        if funcao == '_hash':
            valor_hash = self._hash(key)
        elif funcao == 'hash_primeira_letra':
            valor_hash = self.hash_primeira_letra(key)
        elif funcao == 'hash_nativa':
            valor_hash = self.hash_nativa(key)

        return valor_hash

    def put(self, key, value, funcao):
        novo_no = Node(key, value)
        valor_hash = self.escolher_hash(key, funcao)

        if self.table[valor_hash].insert(novo_no):
            self.n += 1
        
        '''Teste
        aux: Node = self.table[valor_hash]
        if aux == None:
            self.table[valor_hash] = Node(key, value)

        else:
            while aux != None:
                if aux.key == key:
                    aux.value = value
                    return

                if aux.prox == None:
                    aux.prox = Node(key, value)
                    break

                aux = aux.prox 

        self.table[valor_hash].quant += 1
        self.n += 1
        '''

    def get(self, key, funcao):
        valor_hash = self.escolher_hash(key, funcao)

        item = self.table[valor_hash].get(key)

        if item:
            return item
        else:
            return None
        
    def isEmpty(self):
        return self.n == 0
    
def gerar_histograma(eixo_x, ht: HashTable):
    alpha = ht.n/ht.M
    margem_de_erro = 0.10

    colisoes = [ht.table[i].quant if ht.table[i] else 0 for i in range(ht.M) ]

    barras = plt.bar(eixo_x, colisoes)
    plt.bar_label(barras, colisoes)

    plt.xticks(eixo_x)

    plt.axhline(y=alpha, color='black', linestyle='dashed', label="fator de carga")
    plt.axhline(y=alpha*(1 + margem_de_erro), color='red', linestyle='dashed')
    plt.axhline(y=alpha*(1 - margem_de_erro), color='red', linestyle='dashed', alpha=1)
    
    eixo_y = [i for i in range(0, max(colisoes) + 1, max(colisoes)//10)]
    eixo_y.append(alpha)
    eixo_y.sort()
    plt.yticks(eixo_y)

    #plt.grid(axis='y', linestyle="dashed")
    plt.tight_layout()
    plt.legend()
    plt.show()

def montar_HashTable(hashtable: HashTable, array, funcao):
    for i in range(len(array)):
        n = array[i]
        #inserir elemento cuja chave é a palavra e valor é o index
        hashtable.put(n, i, funcao)

'''Maioria apenas testes no main'''
if __name__ == '__main__':
    #letras do alfabeto
    letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    nomes = carregar_nomes("alunosED_2026.txt", por_linha = True)

    #cria a hashtable com o M
    ht_1L = HashTable(26)
    ht_17 = HashTable(17)
    
    #monta ela com base em uma array e a funcao escolhida
    montar_HashTable(ht_1L, nomes, "hash_nativa")
    
    clara_dos_anjos = carregar_nomes("clara-dos-anjos.txt", por_linha = False)
    montar_HashTable(ht_17, clara_dos_anjos, "_hash")

    #gera os graficos, para os que exige o alfabeto usa o 'letras'
    #para os outros gera uma lista com a quantidade de itens do balde
    gerar_histograma(letras, ht_1L)
    gerar_histograma([i for i in range(1, 17 + 1)], ht_17)
    #gerar_histograma([i for i in range(17)], ht_classe_17)
    #gerar_histograma([i for i in range(43)], ht_classe_43)