import sys
import networkx as nx


def carregar_grafo(path):
    """
    Lê arquivo .mc no formato:
    c ... (comentários)
    p edge NUM_VERTICES NUM_ARESTAS
    e u v

    Retorna um grafo não-direcionado.
    """
    G = nx.Graph()

    with open(path, "r") as f:
        for linha in f:
            linha = linha.strip()

            if linha.startswith("c"):
                continue

            if linha.startswith("p"):
                _, _, n, _ = linha.split()
                G.add_nodes_from(range(1, int(n) + 1))
                continue

            if linha.startswith("e"):
                _, u, v = linha.split()
                G.add_edge(int(u), int(v))

    return G


def sahni_gonzalez_maxcut(G):
    """
    Heurística de Sahni–Gonzalez para Max-Cut.
    Retorna os conjuntos A e B.
    """

    # dois conjuntos inicialmente vazios
    A = set()
    B = set()

    # processa os vértices em ordem crescente
    for v in sorted(G.nodes()):

        # contagem de arestas que aumentariam o corte se v for para A
        ganho_A = sum(1 for u in G.neighbors(v) if u in B)

        # contagem se v for para B
        ganho_B = sum(1 for u in G.neighbors(v) if u in A)

        # decide onde colocar
        if ganho_A > ganho_B:
            A.add(v)
        elif ganho_B > ganho_A:
            B.add(v)
        else:
            # empate → coloque no menor conjunto ou no A para consistência
            if len(A) <= len(B):
                A.add(v)
            else:
                B.add(v)

    return A, B


def tamanho_corte(G, A, B):
    """
    Conta número de arestas entre A e B.
    """
    return sum(1 for u, v in G.edges() if (u in A and v in B) or (u in B and v in A))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python maxcut.py arquivo.mc")
        sys.exit(1)

    arquivo = sys.argv[1]

    # caso esteja rodando dentro da pasta labs igual dominantes/coloração
    if "\\" not in arquivo and "/" not in arquivo:
        arquivo = "labs/" + arquivo

    G = carregar_grafo(arquivo)

    A, B = sahni_gonzalez_maxcut(G)

    corte = tamanho_corte(G, A, B)

    print(f"Tamanho do corte: {corte}")
    print(f"Conjunto A ({len(A)} vértices): {sorted(A)}")
    print(f"Conjunto B ({len(B)} vértices): {sorted(B)}")
