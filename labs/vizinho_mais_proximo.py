#!/usr/bin/env python3
"""
tsp_nn.py

Heurística do Vizinho Mais Próximo para instâncias TSPLIB (.tsp).
- Lê instâncias no formato TSPLIB com NODE_COORD_SECTION.
- Calcula distâncias Euclidianas (arredonda conforme TSPLIB quando pedido).
- Dois modos:
    * --start K : começa sempre no vértice K (1-indexado)
    * --try-all : tenta todos os vértices como início e retorna a melhor rota encontrada
- Saída: imprime custo total e sequência de vértices (1-indexados)

Uso:
    python tsp_nn.py arquivo.tsp
    python tsp_nn.py arquivo.tsp --start 1
    python tsp_nn.py arquivo.tsp --try-all
"""

import sys
import math
import argparse

def ler_tsp(path):
    """
    Lê um arquivo .tsp (formato TSPLIB) e retorna dicionário {node: (x,y)}
    Suporta instâncias com seção NODE_COORD_SECTION e formatação padrão.
    Não implementa todos os tipos TSPLIB — suficiente para a maioria das instâncias Euclidianas.
    """
    coords = {}
    in_section = False
    with open(path, "r") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            # ignora comentários que comecem com 'COMMENT' ou 'EOF'
            if linha.upper().startswith("EOF"):
                break
            if linha.upper().startswith("NODE_COORD_SECTION"):
                in_section = True
                continue
            if not in_section:
                continue
            # aqui estamos dentro da seção de coordenadas
            parts = linha.split()
            # espera: index x y  (às vezes há um 4º campo)
            try:
                idx = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                coords[idx] = (x, y)
            except Exception as e:
                # pula linhas mal formatadas
                continue
    return coords

def euclid_dist(a, b):
    """Distância Euclidiana entre pontos a=(x,y) e b=(x,y)."""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def construir_matriz_distancias(coords, use_round=False):
    """
    Constrói uma matriz (dicionário) de distâncias entre vértices.
    use_round: se True, aplica arredondamento típico do TSPLIB (floor(d + 0.5))
    Retorna: dist[u][v]
    """
    nodes = sorted(coords.keys())
    dist = {u: {} for u in nodes}
    for i in nodes:
        for j in nodes:
            if i == j:
                dist[i][j] = 0.0
            else:
                d = euclid_dist(coords[i], coords[j])
                if use_round:
                    d = float(int(d + 0.5))
                dist[i][j] = d
    return dist

def nearest_neighbor_tour(dist, start):
    """
    Gera um tour usando heurística do vizinho mais próximo iniciando em `start`.
    dist: dicionário de distâncias dist[u][v]
    start: índice do vértice inicial (deve estar nas chaves de dist)
    Retorna: (custo_total, lista_ordem_visita)
    """
    nodes = list(dist.keys())
    n = len(nodes)
    visited = set([start])
    tour = [start]
    current = start
    total_cost = 0.0

    # enquanto houver nós não visitados, escolhe o mais próximo
    while len(visited) < n:
        # procurar o vizinho não visitado de menor distância
        best = None
        best_d = float("inf")
        for v in nodes:
            if v in visited:
                continue
            d = dist[current][v]
            if d < best_d:
                best_d = d
                best = v
            # em caso de empate por distância exata, o for com nodes ordenados
            # garante menor índice se nodes estiver ordenado.
        # avança para o melhor vizinho
        tour.append(best)
        visited.add(best)
        total_cost += best_d
        current = best

    # volta ao início (fecha o ciclo)
    total_cost += dist[current][start]
    tour.append(start)  # opcional: para mostrar que voltou ao início
    return total_cost, tour

def executar(args):
    # 1) ler coordenadas
    coords = ler_tsp(args.file)
    if not coords:
        print("Erro: não consegui ler coordenadas do arquivo.", file=sys.stderr)
        sys.exit(1)

    # 2) construir matriz de distâncias
    dist = construir_matriz_distancias(coords, use_round=args.round)

    # 3) modo de execução
    best_cost = float("inf")
    best_tour = None

    starts = []
    if args.try_all:
        starts = sorted(coords.keys())  # tenta todos os nós como início
    else:
        # usar nó indicado (ou 1 por padrão se não indicado)
        s = args.start if args.start is not None else min(coords.keys())
        if s not in coords:
            print(f"Erro: vértice inicial {s} não está presente na instância.", file=sys.stderr)
            sys.exit(1)
        starts = [s]

    # 4) executar NN para cada início em 'starts'
    for s in starts:
        cost, tour = nearest_neighbor_tour(dist, s)
        # se for melhor, guarda
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    # 5) imprimir resultado (formato simples)
    # Mostramos custo e sequência (sem o retorno final repetido, se preferir).
    print(f"Custo total: {best_cost}")
    # remover último elemento que repete o início para exibir ciclo como sequência simples
    if best_tour and best_tour[0] == best_tour[-1]:
        simple_tour = best_tour[:-1]
    else:
        simple_tour = best_tour
    print("Tour (ordem de visita):")
    print(" ".join(str(x) for x in simple_tour))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heurística NN para instâncias TSP (formato TSPLIB).")
    parser.add_argument("file", help="arquivo .tsp (TSPLIB) a ser resolvido")
    parser.add_argument("--start", type=int, help="vértice inicial (1-indexado). Se omitido, usa menor índice.")
    parser.add_argument("--try-all", action="store_true", help="tentar todos os vértices como início e escolher a melhor solução")
    parser.add_argument("--round", action="store_true", help="usar arredondamento TSPLIB (floor(d + 0.5)) nas distâncias")
    args = parser.parse_args()
    executar(args)
