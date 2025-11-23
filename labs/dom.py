import sys
import networkx as nx
# Ele tenta escolher vértices que dominam muitos outros de uma vez, reduzindo o tamanho de S.
def carregar_grafo(path):
    G = nx.Graph()

    with open(path, "r") as f:
        for linha in f:
            linha = linha.strip()

            # ignora comentários
            if linha.startswith("c"):
                continue

            # linha do número de vértices
            if linha.startswith("p"):
                parts = linha.split()
                n_vertices = int(parts[2])
                G.add_nodes_from(range(1, n_vertices + 1))
                continue

            # linhas de arestas
            if linha.startswith("e"):
                _, u, v = linha.split()
                G.add_edge(int(u), int(v))

    return G


def conjunto_dominante_aproximado(G):
    # C começa como todos os vértices
    C = set(G.nodes())
    # conjunto dominante resultante
    S = set()

    # dicionário de dominados
    dominado = {v: False for v in G.nodes()}

    while C:
        # calcula, para cada v em C, quantos vizinhos NÃO dominados ele tem
        melhor_v = None
        melhor_qtd = -1

        for v in sorted(C):  # sorted garante menor índice em empate
            viz_nao_dom = sum(1 for u in G.neighbors(v) if not dominado[u])
            if viz_nao_dom > melhor_qtd:
                melhor_qtd = viz_nao_dom
                melhor_v = v

        v = melhor_v #vertice que domina mais vertices nao dominados

        # verificar se v ou algum vizinho não está dominado
        precisa_inserir = (not dominado[v]) or any(not dominado[u] for u in G.neighbors(v))

        if precisa_inserir:
            S.add(v)
            # marca v e seus vizinhos como dominados
            dominado[v] = True
            for u in G.neighbors(v):
                dominado[u] = True

        # remove v de C
        C.remove(v)

    return sorted(S)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python dom.py arquivo.col")
        sys.exit(1)

    arquivo = sys.argv[1]   # ex: le450_5a.col



    G = carregar_grafo(arquivo)
    S = conjunto_dominante_aproximado(G)

    # imprime no formato solicitado
    print(len(S), "(", *S, ")")
