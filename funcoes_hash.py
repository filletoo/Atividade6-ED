import re
import matplotlib.pyplot as plt

def carregar_nomes(arquivo):
    with open(arquivo, mode='r', encoding="utf-8") as f:
        texto = f.read().lower()
        nomes = re.split(r'[,.;:/—!?()" ]+', texto)

    return nomes

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

def ht_com_funcao_classe(M, palavras):
    ht = HashTable(M)
    for n in palavras:
        valor_hash = ht._hash(n)
        if ht.table[valor_hash] == None:
            ht.table[valor_hash] = []

        if n not in ht.table[valor_hash]:
            ht.table[valor_hash].append(n)
            ht.n += 1

    return ht

def gerar_histograma(eixo_x, ht: HashTable):
    alpha = ht.n/ht.M
    margem_de_erro = 0.10

    colisoes = [len(ht.table[i]) for i in range(ht.M)]

    plt.figure(figsize=(70, 30))
    barras = plt.bar(eixo_x, colisoes)
    plt.xticks(eixo_x)
    plt.axhline(y=alpha, color='black')
    plt.axhline(y=alpha*(1 + margem_de_erro), color='red')
    plt.axhline(y=alpha*(1 - margem_de_erro), color='red')
    plt.show()

if __name__ == '__main__':
    #letras do alfabeto
    letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    nomes = carregar_nomes("alunosED_2026.txt")

    #Usando a primeira letra e M = 26
    ht_1L = HashTable(26)

    for n in nomes:
        valor_hash = ht_1L.hash_primeira_letra(n)
        if ht_1L.table[valor_hash] == None:
            ht_1L.table[valor_hash] = []

        ht_1L.table[valor_hash].append(n)
        ht_1L.n += 1

    #Usando a hash do python e M = 26
    ht_nativa = HashTable(26)

    for n in nomes:
        valor_hash = hash(n) % 26
        if ht_nativa.table[valor_hash] == None:
            ht_nativa.table[valor_hash] = []

        ht_nativa.table[valor_hash].append(n)
        ht_nativa.n += 1

    clara_dos_anjos = carregar_nomes("clara-dos-anjos.txt")

    #Usando a hash da classe e M = 17, 43, 97
    ht_classe_17 = ht_com_funcao_classe(17, clara_dos_anjos)
    ht_classe_43 = ht_com_funcao_classe(43, clara_dos_anjos)
    ht_classe_97 = ht_com_funcao_classe(97, clara_dos_anjos)

    #Usando a hash da classe e M = 16, 40, 100
    ht_classe_16 = ht_com_funcao_classe(16, clara_dos_anjos)
    ht_classe_40 = ht_com_funcao_classe(40, clara_dos_anjos)
    ht_classe_100 = ht_com_funcao_classe(100, clara_dos_anjos)

    gerar_histograma(letras, ht_1L)
    gerar_histograma(letras, ht_nativa)
    gerar_histograma([i for i in range(17)], ht_classe_17)
    gerar_histograma([i for i in range(43)], ht_classe_43)