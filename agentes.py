"""
agentes.py
Estos son tres agentes que resuelven el laberinto
Usamos BFS, A* y Greedy 
"""

from collections import deque
import heapq


def vecinos_validos(fila, col, grilla, filas, cols):
    # devuelve las que no sean pared
    resultado = []
    for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nf = fila + df
        nc = col + dc
        if 0 <= nf < filas and 0 <= nc < cols:
            if grilla[nf][nc] == 0:
                resultado.append((nf, nc))
    return resultado


def reconstruir_camino(padres, meta):
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.reverse()
    return camino



# Agente 1 - BFS

def bfs(laberinto):
    grilla = laberinto["grilla"]
    filas = laberinto["filas"]
    cols = laberinto["columnas"]
    inicio = laberinto["inicio"]
    meta = laberinto["meta"]

    cola = deque([inicio])
    visitados = {inicio}
    padres = {inicio: None}
    explorados = 0

    while cola:
        actual = cola.popleft()
        explorados += 1

        if actual == meta:
            camino = reconstruir_camino(padres, meta)
            return {"exito": True, "camino": camino, "nodos_explorados": explorados}

        for v in vecinos_validos(*actual, grilla, filas, cols):
            if v not in visitados:
                visitados.add(v)
                padres[v] = actual
                cola.append(v)

    return {"exito": False, "camino": [], "nodos_explorados": explorados}




# Agente 2 - A* usa distancia Manhattan como heuristica

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(laberinto):
    grilla = laberinto["grilla"]
    filas = laberinto["filas"]
    cols = laberinto["columnas"]
    inicio = laberinto["inicio"]
    meta = laberinto["meta"]

    heap = [(manhattan(inicio, meta), inicio)]
    padres = {inicio: None}
    costo_g = {inicio: 0}
    explorados = 0

    while heap:
        _, actual = heapq.heappop(heap)
        explorados += 1

        if actual == meta:
            camino = reconstruir_camino(padres, meta)
            return {"exito": True, "camino": camino, "nodos_explorados": explorados}

        for v in vecinos_validos(*actual, grilla, filas, cols):
            nuevo_g = costo_g[actual] + 1
            if v not in costo_g or nuevo_g < costo_g[v]:
                costo_g[v] = nuevo_g
                f = nuevo_g + manhattan(v, meta)
                heapq.heappush(heap, (f, v))
                padres[v] = actual

    return {"exito": False, "camino": [], "nodos_explorados": explorados}



# Agente 3 - Greedy

def greedy(laberinto):
    grilla = laberinto["grilla"]
    filas = laberinto["filas"]
    cols = laberinto["columnas"]
    inicio = laberinto["inicio"]
    meta = laberinto["meta"]

    heap = [(manhattan(inicio, meta), inicio)]
    padres = {inicio: None}
    visitados = {inicio}
    explorados = 0

    while heap:
        _, actual = heapq.heappop(heap)
        explorados += 1

        if actual == meta:
            camino = reconstruir_camino(padres, meta)
            return {"exito": True, "camino": camino, "nodos_explorados": explorados}

        for v in vecinos_validos(*actual, grilla, filas, cols):
            if v not in visitados:
                visitados.add(v)
                padres[v] = actual
                heapq.heappush(heap, (manhattan(v, meta), v))

    return {"exito": False, "camino": [], "nodos_explorados": explorados}