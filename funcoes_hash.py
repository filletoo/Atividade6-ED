import re
import matplotlib.pyplot as plt

ALFABETO = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
funcoes_hash = ["_hash", "hash_primeira_letra", "hash_nativa"]
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prox = None
    
class HashListaLigada:
    def __init__(self):
        self.inicio = None
        self.quant = 0

    def insert(self, novo_no):
        atual = self.inicio

        while atual is not None:
            if atual.key == novo_no.key:
                atual.value = novo_no.value
                return False
            atual = atual.prox
        novo_no.prox = self.inicio
        self.inicio = novo_no
        self.quant += 1
        return True
    
    def get(self, key):
        atual = self.inicio
        while atual is not None:
            if atual.key == key:
                return atual.value
            atual = atual.prox
        return None

    def isEmpty(self):
        return self.quant == 0
    
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

        if self.table[valor_hash] == None:
            self.table[valor_hash] = HashListaLigada()

        if self.table[valor_hash].insert(novo_no):
            self.n += 1
        
    def get(self, key, funcao):
        valor_hash = self.escolher_hash(key, funcao)

        lista = self.table[valor_hash]
        if lista == None: 
            return None

        return self.table[valor_hash].get(key)

    def isEmpty(self):
        return self.n == 0

def gerar_histograma(ht: HashTable, nome_do_grafico, eixo_x = None):
    alpha = ht.n/ht.M
    plt.figure(figsize=(1000, 480, 'px'))
    if not eixo_x:
        eixo_x = [i for i in range(ht.M)]
    
    colisoes = [ht.table[i].quant if ht.table[i] else 0 for i in range(ht.M)]

    margem_de_erro = 2*((alpha)**(1/2))
    barras = plt.bar(eixo_x, colisoes)
    plt.bar_label(barras, colisoes, padding=2, fontsize=8)

    if len(eixo_x) >= 80:
        eixo_x = eixo_x[::2]

    
    plt.xticks(eixo_x)
    plt.title(nome_do_grafico)

    plt.axhline(y=alpha, color="#3b3b3b", linestyle='dashed', label="Fator de carga")
    plt.axhline(y=alpha + margem_de_erro, color='red', linestyle='dashed', label=f"Margem de erro ({margem_de_erro/alpha*100:.2f}%)")
    plt.axhline(y=alpha - margem_de_erro, color='red', linestyle='dashed')

    #para caso tente ser gerado o histograma de uma HashTable sem item
    if ht.n != 0: 
        eixo_y = [i for i in range(0, max(colisoes) + 1, max(colisoes)//10)]
        eixo_y.append(alpha)
        eixo_y.sort()
    
        #remover algum valor que esteja perto do fator de carga
        index_alpha = eixo_y.index(alpha)
        if 0 <= index_alpha - 1 < len(eixo_y) and alpha - eixo_y[index_alpha - 1] < 5:
            eixo_y.pop(eixo_y.index(alpha) - 1)

        index_alpha = eixo_y.index(alpha)
        if 0 <= index_alpha + 1 < len(eixo_y) and eixo_y[index_alpha + 1] - alpha < 5:
            eixo_y.pop(eixo_y.index(alpha) + 1)
    
        plt.yticks(eixo_y)

    #plt.grid(axis='y', linestyle="dashed")
    plt.ylabel("Colisões")
    plt.xlabel("Valores Hash")
    plt.tight_layout()
    plt.legend()
    plt.show()

def montar_HashTable(hashtable: HashTable, array, funcao):
    for i in range(len(array)):
        n = array[i]
        #print(n)
        #inserir elemento cuja chave é a palavra e valor é o index
        hashtable.put(n, i, funcao)

# Arquivo, leitura por linha, nome da função hash no arquivo original e valores de M.
def carregar_entradas(caminho, por_linha):
    """Faz a leitura sem perder as últimas entradas do arquivo.
    """
    with open(caminho, mode='r', encoding='utf-8') as f:
        texto = f.read().lower().strip()
        if por_linha:
            return [linha.strip() for linha in texto.splitlines() if linha.strip()]

        partes = re.split(r"[@,.;:/—!?()\n–\- ]+", texto)
        return [palavra.strip() for palavra in partes if palavra.strip()]

def mostrar_menu():
    print("\n========== EXPERIMENTOS ==========")
    print("1 - Arquivo 'alunosED_2026.txt': Primeira letra (M = 26)")
    print("2 - Arquivo 'alunosED_2026.txt': Hash nativa (M = 26)")
    print("3 - Arquivo 'clara-dos-anjos.txt': Hash da classe (M = 17, 43, 97)")
    print("4 - Arquivo 'clara-dos-anjos.txt': Hash da classe (M = 16, 40, 100)")
    print("5 - Experimento personalizado")
    print("0 - Sair")

def main():
    try:
        nomes = carregar_entradas('alunosED_2026.txt', True)
    except FileNotFoundError:
        print("'alunosED_2026.txt'não pôde ser encontrado.")
        return

    try:
        clara_dos_anjos = carregar_entradas('clara-dos-anjos.txt', False)
    except FileNotFoundError:
        print("'clara-dos-anjos.txt' não pôde ser encontrado.")
        return 
    
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            ht = HashTable(26)
            montar_HashTable(ht, nomes, funcao="hash_primeira_letra")
            gerar_histograma(ht, "'alunosED_2026.txt'. Hash primeira letra. M = 26", ALFABETO)

        elif opcao == '2':
            ht = HashTable(26)
            montar_HashTable(ht, nomes, funcao="hash_nativa")
            gerar_histograma(ht, "'alunosED_2026.txt'. Hash nativa. M = 26", ALFABETO)

        elif opcao == '3':
            numeros = [17, 43, 97]
            
            tabelas_hash = []
            for i in numeros:
                ht = HashTable(i)
                montar_HashTable(ht, clara_dos_anjos, funcao="_hash")
                tabelas_hash.append(ht)

            for i in range(len(tabelas_hash)):
                M = numeros[i]
                ht = tabelas_hash[i]
                gerar_histograma(ht, f"'clara-dos-anjos.txt'. Hash da classe. M = {M}")

        elif opcao == '4':
            numeros = [16, 40, 100]
            tabelas_hash = []
            for i in numeros:
                ht = HashTable(i)
                montar_HashTable(ht, clara_dos_anjos, funcao="_hash")
                tabelas_hash.append(ht)

            for i in range(len(tabelas_hash)):
                M = numeros[i]
                ht = tabelas_hash[i]
                gerar_histograma(ht, f"'clara-dos-anjos.txt'. Hash da classe. M = {M}")

        elif opcao == '5':
            while True:
                arquivo = input("- Arquivo do qual deseja montar a tabela hash (leitura por palavra):\n ").strip()
                try:
                    dados = carregar_entradas(arquivo, False)
                    break
                except FileNotFoundError:
                    print("O arquivo não pode ser encontrado.\n")

            while True:
                try:
                    M = int(input("- M: "))
                    if M <= 0:
                        print("M deve ser positivo.\n")
                    else:
                        break
                except ValueError:
                    print("M deve ser um número inteiro.\n")

            ht = HashTable(M)
            while True:
                opcao = input('''1 - Hash da classe\n2 - Hash da primeira letra\n3 - Hash nativa\nOpcao: ''')
                if opcao == '1':
                    funcao = "_hash"
                elif opcao == '2':
                    funcao = "hash_primeira_letra"
                elif opcao == '3':
                    funcao = "hash_nativa"
                else:
                    print("Escolha uma opção válida.\n")
                    continue

                break

            montar_HashTable(ht, dados, funcao)
            gerar_histograma(ht, f"'{arquivo}'. {funcao}. M = {M}")

        elif opcao == "0":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
