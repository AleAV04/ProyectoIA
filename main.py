"""
main.py
Corre los 3 agentes sobre los 25 laberintos del benchmark en 3 fases:
  Fase 1: 10 laberintos 5x5
  Fase 2: 10 laberintos 10x10
  Fase 3: 5 laberintos 15x15

Incluye un Score Compuesto (0-100) por fase y resumen final.
"""

import csv
import statistics
import matplotlib.pyplot as plt

from benchmark import crear_benchmark
from agentes   import bfs, astar, greedy
from metricas  import medir


# ─────────────────────────────────────────────────────────────────────────────
# SCORE COMPUESTO  (siempre entre 0 y 100)
#
# Cada metrica se normaliza a [0,1] donde 1 = mejor, 0 = peor.
# Luego se pondera:
#   Exito   40%  — llega a la meta?
#   Pasos   30%  — que tan corto es el camino?
#   Nodos   20%  — cuantas celdas exploro?
#   Tiempo  10%  — que tan rapido corrio?
# ─────────────────────────────────────────────────────────────────────────────

PESOS = {"exito": 0.40, "pasos": 0.30, "nodos": 0.20, "tiempo": 0.10}

def calcular_score_compuesto(resumen):
    nombres = list(resumen.keys())
    raw = {
        "exito":  {n: resumen[n]["tasa_exito_%"] / 100     for n in nombres},
        "pasos":  {n: resumen[n]["promedio_pasos"] or 0    for n in nombres},
        "nodos":  {n: resumen[n]["promedio_nodos"]         for n in nombres},
        "tiempo": {n: resumen[n]["promedio_tiempo_ms"]     for n in nombres},
    }

    def norm_mayor(d):   # mayor = mejor (exito)
        mn, mx = min(d.values()), max(d.values())
        return {k: 1.0 for k in d} if mx == mn else {k: (v-mn)/(mx-mn) for k,v in d.items()}

    def norm_menor(d):   # menor = mejor (pasos, nodos, tiempo)
        mn, mx = min(d.values()), max(d.values())
        return {k: 1.0 for k in d} if mx == mn else {k: (mx-v)/(mx-mn) for k,v in d.items()}

    norm = {
        "exito":  norm_mayor(raw["exito"]),
        "pasos":  norm_menor(raw["pasos"]),
        "nodos":  norm_menor(raw["nodos"]),
        "tiempo": norm_menor(raw["tiempo"]),
    }
    return {n: round(sum(PESOS[m] * norm[m][n] for m in PESOS) * 100, 1) for n in nombres}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def calcular_resumen(filas, agentes):
    resumen = {}
    for nombre in agentes:
        fa = [f for f in filas if f["agente"] == nombre]
        pasos_ok = [f["pasos"] for f in fa if f["pasos"] != "N/A"]
        resumen[nombre] = {
            "tasa_exito_%":       round(sum(f["exito"] for f in fa) / len(fa) * 100, 1),
            "promedio_pasos":     round(statistics.mean(pasos_ok), 2) if pasos_ok else 0,
            "promedio_tiempo_ms": round(statistics.mean(f["tiempo_ms"] for f in fa), 4),
            "promedio_nodos":     round(statistics.mean(f["nodos_explorados"] for f in fa), 1),
        }
    return resumen


def ordenar_por_score(nombres, scores):
    return sorted(nombres, key=lambda n: scores[n], reverse=True)


def ganador_o_empate(nombres, key_fn, menor_es_mejor=False):
    vals = {n: key_fn(n) for n in nombres}
    mejor_val = min(vals.values()) if menor_es_mejor else max(vals.values())
    ganadores = [n for n, v in vals.items() if v == mejor_val]
    if len(ganadores) == len(nombres):
        return "Empate (todos)"
    return ganadores[0] if len(ganadores) == 1 else f"Empate ({'/'.join(ganadores)})"


def imprimir_tabla(resumen, scores, titulo):
    nombres  = ordenar_por_score(list(resumen.keys()), scores)
    POSICIONES = ["1ro", "2do", "3ro"]
    print(f"\n{'=' * 73}")
    print(f"  {titulo}")
    print(f"{'=' * 73}")
    print(f"  {'':4} {'Agente':<8}  {'Exito':>7}  {'Pasos':>7}  {'Tiempo(ms)':>11}  {'Nodos':>7}  {'Score /100':>10}")
    print(f"  {'-' * 67}")
    for i, n in enumerate(nombres):
        d = resumen[n]
        pos = POSICIONES[i] if i < 3 else "   "
        print(f"  {pos}  {n:<8}  {d['tasa_exito_%']:>6.1f}%  "
              f"{d['promedio_pasos']:>7.1f}  "
              f"{d['promedio_tiempo_ms']:>11.4f}  "
              f"{d['promedio_nodos']:>7.1f}  "
              f"{scores[n]:>10.1f}")
    print(f"{'=' * 73}")
    ganador = nombres[0]
    print(f"  >> Mejor agente: {ganador}  (Score {scores[ganador]:.1f} / 100)")
    print(f"{'=' * 73}")


def imprimir_conclusion_final(resumen, scores, s1, s2, s3):
    """
    Un solo bloque al final que explica con numeros reales:
    - quien gano en cada metrica
    - por que nodos es enganosa en este benchmark
    """
    nombres  = list(resumen.keys())
    nombres_ord = ordenar_por_score(nombres, scores)
    ganador  = nombres_ord[0]

    mejor_nodos = ganador_o_empate(nombres, lambda n: resumen[n]["promedio_nodos"], menor_es_mejor=True)
    mejor_score = ganador_o_empate(nombres, lambda n: scores[n])

    # Datos concretos
    nodos_por_agente = {n: resumen[n]["promedio_nodos"] for n in nombres}
    exito_por_agente = {n: resumen[n]["tasa_exito_%"]   for n in nombres}
    pasos_por_agente = {n: resumen[n]["promedio_pasos"] for n in nombres}

    exitos_iguales = len(set(exito_por_agente.values())) == 1
    exito_val      = list(exito_por_agente.values())[0]

    print(f"\n{'=' * 65}")
    print("  CONCLUSION FINAL")
    print(f"{'=' * 65}")

    # Tabla: quien gano en cada metrica
    print(f"\n  Ganador por metrica (25 laberintos en total):")
    print(f"  {'-' * 47}")
    print(f"  {'Metrica':<28}  {'Ganador':>15}")
    print(f"  {'-' * 47}")
    print(f"  {'Tasa de exito':<28}  {ganador_o_empate(nombres, lambda n: exito_por_agente[n]):>15}")
    print(f"  {'Pasos (calidad del camino)':<28}  {ganador_o_empate(nombres, lambda n: pasos_por_agente[n], True):>15}")
    print(f"  {'Nodos explorados':<28}  {mejor_nodos:>15}")
    print(f"  {'Tiempo de ejecucion':<28}  {ganador_o_empate(nombres, lambda n: resumen[n]['promedio_tiempo_ms'], True):>15}")
    print(f"  {'-' * 47}")
    print(f"  {'Score Compuesto (0-100)':<28}  {mejor_score:>15}")
    print(f"  {'-' * 47}")

    # Tabla completa de datos
    pasos_iguales = len(set(pasos_por_agente.values())) == 1
    diff_score    = scores[nombres_ord[0]] - scores[nombres_ord[-1]]

    print(f"\n  {'Agente':<8}  {'Exito':>8}  {'Pasos':>7}  {'Nodos':>8}  {'Tiempo(ms)':>12}  {'Score':>8}")
    print(f"  {'-' * 58}")
    for n in nombres_ord:
        print(f"  {n:<8}  {exito_por_agente[n]:>7.1f}%  "
              f"{pasos_por_agente[n]:>7.1f}  "
              f"{nodos_por_agente[n]:>8.1f}  "
              f"{resumen[n]['promedio_tiempo_ms']:>12.4f}  "
              f"{scores[n]:>8.1f}")

    # Argumento dinamico: detectar que metrica es enganosa segun los datos reales
    print(f"\n  Metrica enganosa detectada en este benchmark:")
    print(f"  {'-' * 60}")

    ganador_exito = max(nombres, key=lambda n: exito_por_agente[n])

    if exitos_iguales and pasos_iguales:
        # Exito y pasos empatan — tasa de exito es enganosa porque oculta diferencias reales
        print(f"  Tasa de exito: todos tienen {exito_val:.0f}%.")
        print(f"  Vista sola, sugiere que ningun agente es mejor que otro.")
        print(f"  Sin embargo, el Score Compuesto muestra {diff_score:.1f} puntos de diferencia")
        print(f"  entre {nombres_ord[0]} y {nombres_ord[-1]}, capturada por nodos y tiempo.")
        print(f"  -> La tasa de exito oculta diferencias reales de eficiencia.")

    elif exitos_iguales and not pasos_iguales:
        # Exito empata pero pasos no — la tasa de exito no alcanza para decidir
        print(f"  Tasa de exito: todos tienen {exito_val:.0f}%, parece empate total.")
        print(f"  Pero los caminos tienen largo distinto — el Score captura")
        print(f"  esa diferencia de calidad que la tasa de exito no ve.")
        print(f"  -> Una metrica que empata no sirve para elegir.")

    elif not exitos_iguales and ganador_exito != ganador:
        # Exito diferencia, pero el ganador en exito NO es el mejor en Score
        print(f"  {ganador_exito} tiene la mejor tasa de exito ({exito_por_agente[ganador_exito]:.0f}%),")
        print(f"  pero el Score Compuesto elige a {ganador} como mejor agente")
        print(f"  porque su eficiencia compensa la diferencia en llegadas.")
        print(f"  -> Optimizar solo exito puede ignorar la calidad real del agente.")

    else:
        # Todas las metricas apuntan al mismo ganador — no hay contradiccion
        print(f"  En este benchmark todas las metricas apuntan al mismo ganador.")
        print(f"  El Score Compuesto confirma a {ganador} sin contradicciones.")
        print(f"  -> El valor del Score esta en que lo verifico matematicamente.")

    print(f"\n  Mejor agente: {ganador} ({scores[ganador]:.1f}/100).")
    print(f"{'=' * 65}\n")


def generar_grafica(resumen, scores, titulo, archivo):
    nombres = ordenar_por_score(list(resumen.keys()), scores)
    colores = ["#2ecc71", "#3498db", "#e74c3c"]

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    fig.suptitle(titulo, fontsize=13, fontweight="bold")

    metricas_graf = [
        ("Tasa de exito (%)",                  [resumen[n]["tasa_exito_%"]   for n in nombres], "%",     105),
        ("Promedio de pasos\n(menos = mejor)",  [resumen[n]["promedio_pasos"] for n in nombres], "Pasos", None),
        ("Nodos explorados\n(metrica enganosa)",[resumen[n]["promedio_nodos"] for n in nombres], "Nodos", None),
        ("Score Compuesto\n(0-100)",            [scores[n]                   for n in nombres], "Score", 105),
    ]

    for ax, (titulo_ax, vals, ylabel, ylim) in zip(axes, metricas_graf):
        ax.bar(nombres, vals, color=colores[:len(nombres)], edgecolor="white", linewidth=1.2)
        ax.set_title(titulo_ax, fontsize=10, pad=8)
        ax.set_ylabel(ylabel, fontsize=9)
        maxv = max(vals) if max(vals) > 0 else 1
        ax.set_ylim(0, ylim if ylim else maxv * 1.20)
        for i, v in enumerate(vals):
            ax.text(i, v + maxv * 0.03, f"{v:.1f}", ha="center", fontsize=9, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig(archivo, dpi=150)
    plt.close()
    print(f"  Grafica guardada: {archivo}")


def correr_fase(labs, agentes, etiqueta):
    filas = []
    for lab in labs:
        for nombre, fn in agentes.items():
            m = medir(fn, lab)
            filas.append({
                "fase":             etiqueta,
                "laberinto_id":     lab["id"],
                "tamanio":          f"{lab['filas']}x{lab['columnas']}",
                "agente":           nombre,
                "exito":            m["exito"],
                "pasos":            m["pasos"] if m["pasos"] is not None else "N/A",
                "tiempo_ms":        m["tiempo_ms"],
                "nodos_explorados": m["nodos_explorados"],
            })
    return filas


def esperar_usuario(msg):
    input(f"\n  >>  {msg}\n     Presiona ENTER para continuar...")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    laberintos = crear_benchmark()

    fase1 = [l for l in laberintos if l["filas"] == 5]
    fase2 = [l for l in laberintos if l["filas"] == 10]
    fase3 = [l for l in laberintos if l["filas"] == 15]

    agentes = {"BFS": bfs, "A*": astar, "Greedy": greedy}
    todas = []

    # FASE 1
    esperar_usuario("FASE 1 — 10 laberintos pequenos (5x5)")
    print("\n  Corriendo Fase 1...")
    f1 = correr_fase(fase1, agentes, "5x5")
    todas.extend(f1)
    r1 = calcular_resumen(f1, agentes)
    s1 = calcular_score_compuesto(r1)
    imprimir_tabla(r1, s1, "FASE 1 — Laberintos 5x5 (pequenos)")
    generar_grafica(r1, s1, "Fase 1: Laberintos 5x5", "grafica_fase1.png")

    # FASE 2
    esperar_usuario("FASE 2 — 10 laberintos medianos (10x10)")
    print("\n  Corriendo Fase 2...")
    f2 = correr_fase(fase2, agentes, "10x10")
    todas.extend(f2)
    r2 = calcular_resumen(f2, agentes)
    s2 = calcular_score_compuesto(r2)
    imprimir_tabla(r2, s2, "FASE 2 — Laberintos 10x10 (medianos)")
    generar_grafica(r2, s2, "Fase 2: Laberintos 10x10", "grafica_fase2.png")

    # FASE 3
    esperar_usuario("FASE 3 — 5 laberintos grandes (15x15)")
    print("\n  Corriendo Fase 3...")
    f3 = correr_fase(fase3, agentes, "15x15")
    todas.extend(f3)
    r3 = calcular_resumen(f3, agentes)
    s3 = calcular_score_compuesto(r3)
    imprimir_tabla(r3, s3, "FASE 3 — Laberintos 15x15 (grandes)")
    generar_grafica(r3, s3, "Fase 3: Laberintos 15x15", "grafica_fase3.png")

    # RESUMEN FINAL
    esperar_usuario("RESUMEN FINAL — todos los 25 laberintos")
    rf = calcular_resumen(todas, agentes)
    sf = calcular_score_compuesto(rf)
    imprimir_tabla(rf, sf, "RESUMEN FINAL — 25 laberintos")
    generar_grafica(rf, sf, "Resumen Final: 25 laberintos", "grafica_final.png")

    # Scores por fase
    nombres_ord = ordenar_por_score(list(agentes.keys()), sf)
    print(f"\n{'=' * 57}")
    print("  SCORES POR FASE — evolucion del desempeno")
    print(f"  (escala 0-100, combina las 4 metricas)")
    print(f"{'=' * 57}")
    print(f"  {'Agente':<8}  {'5x5':>8}  {'10x10':>8}  {'15x15':>8}  {'Global':>8}  Tendencia")
    print(f"  {'-' * 51}")
    for n in nombres_ord:
        tend = "baja" if s3[n] < s1[n] else ("sube" if s3[n] > s1[n] else "igual")
        print(f"  {n:<8}  {s1[n]:>8.1f}  {s2[n]:>8.1f}  {s3[n]:>8.1f}  {sf[n]:>8.1f}  {tend}")
    print(f"{'=' * 57}")

    # Conclusion unica al final
    imprimir_conclusion_final(rf, sf, s1, s2, s3)

    # Guardar CSV
    with open("resultados.csv", "w", newline="") as f:
        campos = ["fase", "laberinto_id", "tamanio", "agente",
                  "exito", "pasos", "tiempo_ms", "nodos_explorados"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(todas)
    print("  Resultados guardados en resultados.csv\n")


if __name__ == "__main__":
    main()