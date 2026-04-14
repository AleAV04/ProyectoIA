"""
main.py
Corre los 3 agentes sobre los 25 laberintos del benchmark,
mide las métricas, guarda resultados y genera una gráfica.
"""

import csv
import statistics
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from benchmark import crear_benchmark
from agentes   import bfs, astar, greedy
from metricas  import medir

# 1. Crear el benchmark

laberintos = crear_benchmark()

agentes = {
    "BFS":    bfs,
    "A*":     astar,
    "Greedy": greedy
}

# 2. Correr todos los agentes en todos
# los laberintos y guardar resultados

filas_csv = []

print("\n Corriendo benchmark...\n")

for lab in laberintos:
    for nombre_agente, fn in agentes.items():
        m = medir(fn, lab)
        fila = {
            "laberinto_id":     lab["id"],
            "tamaño":           f"{lab['filas']}x{lab['columnas']}",
            "agente":           nombre_agente,
            "exito":            m["exito"],
            "pasos":            m["pasos"] if m["pasos"] is not None else "N/A",
            "tiempo_ms":        m["tiempo_ms"],
            "nodos_explorados": m["nodos_explorados"]
        }
        filas_csv.append(fila)


# 3. Guardar CSV

with open("resultados.csv", "w", newline="") as f:
    campos = ["laberinto_id", "tamaño", "agente", "exito", "pasos", "tiempo_ms", "nodos_explorados"]
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(filas_csv)

print("Resultados guardados en resultados.csv\n")


# 4. Calcular resumen por agente

resumen = {}
for nombre in agentes:
    filas_agente = [f for f in filas_csv if f["agente"] == nombre]

    tasa_exito = sum(f["exito"] for f in filas_agente) / len(filas_agente) * 100

    pasos_validos = [f["pasos"] for f in filas_agente if f["pasos"] != "N/A"]
    promedio_pasos = round(statistics.mean(pasos_validos), 2) if pasos_validos else None

    promedio_tiempo = round(statistics.mean(f["tiempo_ms"] for f in filas_agente), 4)

    promedio_nodos = round(statistics.mean(f["nodos_explorados"] for f in filas_agente), 1)

    resumen[nombre] = {
        "tasa_exito_%":        tasa_exito,
        "promedio_pasos":      promedio_pasos,
        "promedio_tiempo_ms":  promedio_tiempo,
        "promedio_nodos":      promedio_nodos
    }


# 5. Imprimir tabla resumen

print("=" * 65)
print(f"{'Agente':<10} {'Éxito%':>8} {'Pasos':>8} {'Tiempo(ms)':>12} {'Nodos':>8}")
print("=" * 65)
for nombre, datos in resumen.items():
    print(f"{nombre:<10} {datos['tasa_exito_%']:>7.1f}% "
          f"{str(datos['promedio_pasos']):>8} "
          f"{datos['promedio_tiempo_ms']:>12.4f} "
          f"{datos['promedio_nodos']:>8.1f}")
print("=" * 65)


# 6. Generar gráfica comparativa

nombres  = list(resumen.keys())
colores  = ["#4C72B0", "#DD8452", "#55A868"]

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle("Comparación de agentes en el benchmark de laberintos", fontsize=14, fontweight="bold")

# Gráfica 1: Tasa de éxito
ejes0 = [resumen[n]["tasa_exito_%"] for n in nombres]
axes[0].bar(nombres, ejes0, color=colores)
axes[0].set_title("Tasa de éxito (%)")
axes[0].set_ylim(0, 110)
axes[0].set_ylabel("%")
for i, v in enumerate(ejes0):
    axes[0].text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=10)

# Gráfica 2: Promedio de pasos (calidad del camino)
ejes1 = [resumen[n]["promedio_pasos"] or 0 for n in nombres]
axes[1].bar(nombres, ejes1, color=colores)
axes[1].set_title("Promedio de pasos (calidad)")
axes[1].set_ylabel("Pasos")
for i, v in enumerate(ejes1):
    axes[1].text(i, v + 0.3, f"{v:.1f}", ha="center", fontsize=10)

# Gráfica 3: Nodos explorados (complejidad)
# ESTA ES LA MÉTRICA ENGAÑOSA:
# Greedy explora pocos nodos pero su camino es más largo
ejes2 = [resumen[n]["promedio_nodos"] for n in nombres]
axes[2].bar(nombres, ejes2, color=colores)
axes[2].set_title("Nodos explorados\n métrica engañosa")
axes[2].set_ylabel("Nodos")
for i, v in enumerate(ejes2):
    axes[2].text(i, v + 0.3, f"{v:.1f}", ha="center", fontsize=10)

plt.tight_layout()
plt.savefig("grafica_comparativa.png", dpi=150)
plt.close()

print("\n Gráfica guardada en grafica_comparativa.png")
print("\n  NOTA: Greedy explora MENOS nodos (parece eficiente),")
print("   pero sus caminos son MÁS LARGOS que BFS y A*.")
print("   → Optimizar 'nodos explorados' no garantiza mejor solución.\n")
