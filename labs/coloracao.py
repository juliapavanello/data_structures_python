import sys
import networkx as nx


def carregar_grafo(path):
    """
    Lê um arquivo .col no formato:
    c comentários
    p edge NUM_VERTICES NUM_ARESTAS
    e u v  (arestas)

    Retorna um grafo NetworkX.
    """
    G = nx.Graph()

    with open(path, "r") as f:
        for linha in f:
            linha = linha.strip()

            # ignora comentários
            if linha.startswith("c"):
                continue

            # linha de definição do problema
            if linha.startswith("p"):
                parts = linha.split()
                n_vertices = int(parts[2])
                G.add_nodes_from(range(1, n_vertices + 1))
                continue

            # linha de aresta
            if linha.startswith("e"):
                _, u, v = linha.split()
                G.add_edge(int(u), int(v))

    return G


def welsh_powell(G):
    """
    Implementação do algoritmo de Welsh & Powell.
    Retorna um dicionário {vertice: cor}.
    """

    # 1. Ordenar vértices por grau (maior → menor)
    vertices_ordenados = sorted(G.nodes(), key=lambda v: G.degree(v), reverse=True)

    # dicionário que guardará a cor de cada vértice
    cor = {v: 0 for v in G.nodes()}   # 0 = não colorido

    cor_atual = 1

    # 2. Enquanto houver vértice não colorido
    while True:
        nao_coloridos = [v for v in vertices_ordenados if cor[v] == 0]
        if not nao_coloridos:
            break  # acabou!

        # escolhe o primeiro vértice não colorido e atribui a cor atual
        v0 = nao_coloridos[0]
        cor[v0] = cor_atual

        # 3. Tenta pintar outros vértices com essa mesma cor
        for v in nao_coloridos[1:]:
            # verifica se v é adjacente a algum vértice já pintado com cor_atual
            conflito = any(cor[u] == cor_atual for u in G.neighbors(v))

            if not conflito:
                cor[v] = cor_atual

        # 4. Passa para a próxima cor
        cor_atual += 1

    return cor


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python coloracao.py arquivo.col")
        sys.exit(1)

    arquivo = sys.argv[1]

    # Caso esteja sendo executado dentro da pasta labs
    if "\\" not in arquivo and "/" not in arquivo:
        arquivo = "labs/" + arquivo

    G = carregar_grafo(arquivo)
    cores = welsh_powell(G)

    num_cores = len(set(cores.values()))

    print(f"Número de cores usadas: {num_cores}")
    print("Coloração (vértice: cor):")
    for v in sorted(cores):
        print(f"{v}: {cores[v]}")
