import networkx as nx
from operator import itemgetter
import string

# --------------------------------------- CONSTRUÇÃO DA SEQUÊNCIA DE DEBRUIJN ------------------------------------------

def construct_debruijn_sequence(grafo):

    debruijn_sequence = str()
    n = grafo.number_of_edges()     # Quantidade de arestas no grafo

    euler_path = list(nx.eulerian_circuit(grafo))   # Lista com a sequência de arestas do caminho de Euler

    # Seleciona somente os primeiros elementos das tuplas na lista contendo as arestas (origem, destino)
    nodes = list(map(itemgetter(0), euler_path))

    for i in range(n):
        digit = nodes[i]                    # Seleciona o vértice na lista
        debruijn_sequence += digit[0]       # Adiciona somente o primeiro símbolo à sequência de DeBruijn,
                                            # excluindo as repetições

    return debruijn_sequence

# ----------------------------------------- CONSTRUÇÃO DO GRAFO DE DEBRUIJN --------------------------------------------

def create_debruijn_graph(sequences):

    t = len(sequences)      # Quantidade de subsequências geradas
    grafo = nx.DiGraph()    # Criação do grafo

    # Para cada combinação possível de pares de subsequências:
    for i in range(t):
        for j in range(t):

            origem = sequences[i]
            destino = sequences[j]

            # Caso particular: com subsequências de tamanho 1 não há como retirar símbolos da origem ou destino
            if t == 2:
                grafo.add_edge(origem, destino)

            # Retira o primeiro símbolo da origem e o último símbolo do destino para testar a igualdade do par restante
            if origem[1:] == destino[:-1]:
                grafo.add_edge(origem, destino)     # Adiciona a aresta no grafo caso as subsequências restantes sejam iguais

    return grafo

# -------------------------------------------- GERADOR DAS SUBSEQUÊNCIAS -----------------------------------------------

def sequences_generator(r, s):

    # Número de subsequências possíveis de tamanho r - 1   --->   s^(r - 1) representações (0 a t)
    t = s ** (r - 1)

    sequences = [''] * t

    # Geração das subsequências (0 a t) convertidas para a base (s) com tamanho (r - 1)
    for i in range(t):
        sequences[i] = conversor_dec_to_any(i, s, r - 1)

    return sequences

# -------------------------------------- CONVERSOR (DECIMAL --> QUALQUER BASE) -----------------------------------------

def conversor_dec_to_any(dec, base, r):

    # Dicionário de símbolos
    dic = string.digits + string.ascii_letters

    if dec < 0:
        sign = -1
    elif dec == 0:
        return dic[0] * r   # Correção para manter a sequência 0 com tamanho fixo (r - 1)
    else:
        sign = 1

    dec *= sign
    digits = list()

    # Conversão para base (s)
    while dec:
        digits.append(dic[dec % base])
        dec = dec // base

    if sign < 0:
        digits.append('-')

    # Correção para manter todas as sequências com tamanho fixo (r - 1)
    while len(digits) < r:
        digits.append('0')

    digits.reverse()

    return ''.join(digits)

# ------------------------------------------------------- MAIN ---------------------------------------------------------

def main():

    # Leitura dos parâmetros r (tamanho das sequências) e s (número de símbolos ou base)
    while True:
        
        try:
            r = int(input('Informe o tamanho das subsequências (r): '))
            s = int(input('Informe o número de símbolos (s): '))
            
            if r <= 1 or s <= 1:
                print('\nTamanho inválido (r <= 1 ou s <= 1), digite novamente: \n')
                continue
            
            break
        
        except ValueError:
            print('\nInsira valores inteiros válidos!\n')        

    # Geração de todas as sequências possíveis de tamanho (r - 1) na base (s)
    sequences = sequences_generator(r, s)

    # Criação do grafo de DeBruijn a partir das sequências
    grafo = create_debruijn_graph(sequences)

    # Construção da sequência de DeBruijn utilizando o caminho de Euler no grafo
    debruijn_sequence = construct_debruijn_sequence(grafo)

    # Exibição do resultado
    print("\nSequência de DeBruijn: " + debruijn_sequence)


if __name__ == '__main__':
    main()
