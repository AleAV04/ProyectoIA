"""
metricas.py
Mide el rendimiento de cada agente y vemos: exito, largo del camino, tiempo y nodos visitados
"""

import time


def medir(agente_fn, laberinto):
    t0 = time.time()
    resultado = agente_fn(laberinto)
    t1 = time.time()

    tiempo_ms = round((t1 - t0) * 1000, 4)

    exito = 1 if resultado["exito"] else 0
    pasos = len(resultado["camino"]) - 1 if resultado["exito"] else None

    return {
        "exito":            exito,
        "pasos":            pasos,
        "tiempo_ms":        tiempo_ms,
        "nodos_explorados": resultado["nodos_explorados"]
    }