"""
agentes.py
Contiene tres agentes que resuelven laberintos:
- BFS: garantiza el camino más corto
- A*: usa heurística para buscar más inteligente
- Greedy: solo mira la meta, no garantiza camino óptimo
"""

from collections import deque
import heapq


def obtener_vecinos(fila, col, grilla, filas, columnas):
    """Devuelve las celdas adyacentes que no son pared."""
    vecinos = []
    for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]:  # arriba, abajo, izq, der
        nf, nc = fila + df, col + dc
        if 0 <= nf < filas and 0 <= nc < columnas:
            if grilla[nf][nc] == 0:
                vecinos.append((nf, nc))
    return vecinos


def reconstruir_camino(padres, meta):
    """Reconstruye el camino desde inicio hasta meta usando el dict de padres."""
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = padres[actual]
    return list(reversed(camino))



# AGENTE 1: BFS (Búsqueda por amplitud)
# Garantiza el camino más corto (menos pasos)

def bfs(laberinto):
    grilla   = laberinto["grilla"]
    filas    = laberinto["filas"]
    columnas = laberinto["columnas"]
    inicio   = laberinto["inicio"]
    meta     = laberinto["meta"]

    cola     = deque([inicio])
    visitado = {inicio}
    padres   = {inicio: None}
    nodos_explorados = 0

    while cola:
        actual = cola.popleft()
        nodos_explorados += 1

        if actual == meta:
            camino = reconstruir_camino(padres, meta)
            return {"exito": True, "camino": camino, "nodos_explorados": nodos_explorados}

        for vecino in obtener_vecinos(*actual, grilla, filas, columnas):
            if vecino not in visitado:
                visitado.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)

    return {"exito": False, "camino": [], "nodos_explorados": nodos_explorados}



# AGENTE 2: A* (A estrella)
# Usa heurística Manhattan para guiar la búsqueda

def heuristica(a, b):
    """Distancia Manhattan entre dos celdas."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(laberinto):
    grilla   = laberinto["grilla"]
    filas    = laberinto["filas"]
    columnas = laberinto["columnas"]
    inicio   = laberinto["inicio"]
    meta     = laberinto["meta"]

    # (f_score, celda)
    heap = [(heuristica(inicio, meta), inicio)]
    padres  = {inicio: None}
    g_score = {inicio: 0}
    nodos_explorados = 0

    while heap:
        _, actual = heapq.heappop(heap)
        nodos_explorados += 1

        if actual == meta:
            camino = reconstruir_camino(padres, meta)
            return {"exito": True, "camino": camino, "nodos_explorados": nodos_explorados}

        for vecino in obtener_vecinos(*actual, grilla, filas, columnas):
            nuevo_g = g_score[actual] + 1
            if vecino not in g_score or nuevo_g < g_score[vecino]:
                g_score[vecino] = nuevo_g
                f = nuevo_g + heuristica(vecino, meta)
                heapq.heappush(heap, (f, vecino))
                padres[vecino] = actual

    return {"exito": False, "camino": [], "nodos_explorados": nodos_explorados}



# AGENTE 3: Greedy (Avaro)
# Solo mira qué tan cerca está de la meta
# Rápido pero NO garantiza el camino más corto

def greedy(laberinto):
    grilla   = laberinto["grilla"]
    filas    = laberinto["filas"]
    columnas = laberinto["columnas"]
    inicio   = laberinto["inicio"]
    meta     = laberinto["meta"]

    heap = [(heuristica(inicio, meta), inicio)]
    padres   = {inicio: None}
    visitado = {inicio}
    nodos_explorados = 0

    while heap:
        _, actual = heapq.heappop(heap)
        nodos_explorados += 1

        if actual == meta:
            camino = reconstruir_camino(padres, meta)
            return {"exito": True, "camino": camino, "nodos_explorados": nodos_explorados}

        for vecino in obtener_vecinos(*actual, grilla, filas, columnas):
            if vecino not in visitado:
                visitado.add(vecino)
                padres[vecino] = actual
                heapq.heappush(heap, (heuristica(vecino, meta), vecino))

    return {"exito": False, "camino": [], "nodos_explorados": nodos_explorados}
