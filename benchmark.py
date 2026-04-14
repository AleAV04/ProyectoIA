"""
benchmark.py
Genera 25 laberintos reproducibles con distintos tamaños y dificultades.
"""

import random

def generar_laberinto(filas, columnas, semilla):
    """
    Genera un laberinto como grilla 2D.
    0 = camino libre
    1 = pared
    El inicio siempre es (0,0) y la meta es (filas-1, columnas-1).
    """
    random.seed(semilla)

    # Empezamos con todo libre
    grilla = [[0] * columnas for _ in range(filas)]

    # Ponemos paredes aleatoriamente (30% del laberinto)
    for f in range(filas):
        for c in range(columnas):
            if (f, c) == (0, 0) or (f, c) == (filas-1, columnas-1):
                continue  # inicio y meta siempre libres
            if random.random() < 0.30:
                grilla[f][c] = 1

    return {
        "id": semilla,
        "filas": filas,
        "columnas": columnas,
        "grilla": grilla,
        "inicio": (0, 0),
        "meta": (filas - 1, columnas - 1)
    }


def crear_benchmark():
    """
    Crea 25 laberintos con variedad de tamaños.
    Pequeños (5x5), medianos (10x10) y grandes (15x15).
    """
    instancias = []

    # 10 laberintos pequeños (fáciles)
    for i in range(10):
        instancias.append(generar_laberinto(5, 5, semilla=100 + i))

    # 10 laberintos medianos
    for i in range(10):
        instancias.append(generar_laberinto(10, 10, semilla=200 + i))

    # 5 laberintos grandes (difíciles)
    for i in range(5):
        instancias.append(generar_laberinto(15, 15, semilla=300 + i))

    print(f"Benchmark creado: {len(instancias)} laberintos")
    return instancias
