"""
metricas.py
Mide el desempeño de cada agente en cada laberinto.
Métricas:
  - exito:            ¿Encontró solución? (1 = sí, 0 = no)
  - pasos:            Largo del camino encontrado
  - tiempo_ms:        Tiempo de ejecución en milisegundos
  - nodos_explorados: Cuántas celdas revisó (complejidad)
"""

import time


def medir(agente_fn, laberinto):
    """
    Corre un agente sobre un laberinto y devuelve todas las métricas.
    agente_fn: (bfs, astar, greedy)
    laberinto: diccionario generado por benchmark.py
    """
    inicio = time.time()
    resultado = agente_fn(laberinto)
    fin = time.time()

    tiempo_ms = (fin - inicio) * 1000  # convertir a milisegundos

    return {
        "exito":            1 if resultado["exito"] else 0,
        "pasos":            len(resultado["camino"]) - 1 if resultado["exito"] else None,
        "tiempo_ms":        round(tiempo_ms, 4),
        "nodos_explorados": resultado["nodos_explorados"]
    }
