"""
benchmark.py
Genera los laberintos para el benchmark. Usamos semillas fijas para que sea reproducible
"""

import random


def generar_laberinto(filas, cols, semilla):
    """
    El 30% de paredes. 0 = libre, 1 = pared
    Inicio en (0,0), meta en la esquina opuesta.
    """
    random.seed(semilla)

    grilla = [[0]*cols for _ in range(filas)]

    for f in range(filas):
        for c in range(cols):
            if (f, c) in [(0,0), (filas-1, cols-1)]:
                continue
            if random.random() < 0.30:
                grilla[f][c] = 1

    return {
        "id":       semilla,
        "filas":    filas,
        "columnas": cols,
        "grilla":   grilla,
        "inicio":   (0, 0),
        "meta":     (filas-1, cols-1)
    }


def crear_benchmark():
    """
    25 laberintos:
    - 10 pequeños  (5x5)
    - 10 medianos  (10x10)
    - 5  grandes   (15x15)
    """
    instancias = []

    for i in range(10):
        instancias.append(generar_laberinto(5, 5, semilla=100+i))

    for i in range(10):
        instancias.append(generar_laberinto(10, 10, semilla=200+i))

    for i in range(5):
        instancias.append(generar_laberinto(15, 15, semilla=300+i))

    print(f"Benchmark creado: {len(instancias)} laberintos")
    return instancias