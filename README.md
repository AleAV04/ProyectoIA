**EIF420-O · Inteligencia Artificial**

# Integrantes
- ALEJANDRO ALFARO VÍQUEZ
- JUSTIN GAMBOA BADILLA
- JIXI MORALES MENDOZA
- JOSUE ALVARADO MENDEZ
- LUIS MADRIGAL CAMACHO


# ProyectoIA — G2: Evaluación de agentes, cómo medir inteligencia sin autoengañarse

> Benchmark reproducible para comparar tres agentes resolviendo laberintos y detectar cuándo una métrica miente.


## Objetivo y Audiencia

La idea principal no es ver quién llega más rápido a la meta, sino entender si las métricas que usamos para medir eso realmente dicen lo que creemos que dicen. Implementamos un benchmark que compara tres agentes clásicos de búsqueda (BFS, A\* y Greedy) sobre laberintos generados aleatoriamente, y mostramos al menos un caso donde confiar en una sola métrica puede llevar a elegir el agente equivocado.

Está dirigido al curso EIF420-O como entrega del PP1, aunque el diseño del benchmark es lo suficientemente general para que cualquiera interesado en evaluación de agentes lo pueda reutilizar.


## Configuración y Requisitos

- **Lenguaje:** Python 3.8+
- **Librerías:** `matplotlib` (para las gráficas)

Instalación:

```bash
pip install matplotlib
```
No se necesita ninguna API key ni configuración adicional. Todo corre localmente.



## Guía de Ejecución

1. Clonar o descomprimir el proyecto en una carpeta local.
2. Instalar la dependencia:
   ```bash
   pip install matplotlib
   ```
3. Ejecutar el benchmark:
   ```bash
   python main.py
   ```
4. El programa corre en 3 fases según el tamaño de los laberintos. Entre cada fase pide presionar Enter para continuar:
   - **Fase 1** — 10 laberintos pequeños (5×5)
   - **Fase 2** — 10 laberintos medianos (10×10)
   - **Fase 3** — 5 laberintos grandes (15×15)
   - **Resumen final** — análisis global de los 25 laberintos

5. Al terminar, el programa genera estos archivos en la misma carpeta:
   - `grafica_fase1.png`, `grafica_fase2.png`, `grafica_fase3.png`, `grafica_final.png` — una figura comparativa por fase
   - `resultados.csv` — tabla completa con todas las métricas por laberinto y agente


## Estructura del proyecto

```
main.py       → corre el benchmark por fases, calcula Score Compuesto y genera gráficas
agentes.py    → implementación de BFS, A* y Greedy
benchmark.py  → genera los 25 laberintos con semilla fija
metricas.py   → mide tiempo, pasos, nodos explorados y éxito
```


## ¿Qué comparamos?

Tres algoritmos de búsqueda sobre laberintos generados aleatoriamente:

- **BFS** — busca nivel por nivel, siempre encuentra el camino más corto
- **A\*** — usa heurística Manhattan más el costo acumulado, también óptimo
- **Greedy** — solo mira qué tan cerca está de la meta, rápido pero no óptimo

Los laberintos son 25 en total: 10 de 5×5, 10 de 10×10 y 5 de 15×15. Todos generados con semillas fijas para que los resultados sean reproducibles.

Las métricas que medimos en cada ejecución son:

| Métrica          | Qué captura                           |
|------------------|---------------------------------------|
| Tasa de éxito    | ¿El agente llegó a la meta?           |
| Pasos            | Qué tan largo fue el camino encontrado|
| Tiempo (ms)      | Cuánto tardó en ejecutarse            |
| Nodos explorados | Cuántas celdas revisó antes de llegar |

Con estas cuatro métricas calculamos un **Score Compuesto (0–100)** que las combina con pesos: éxito 40%, pasos 30%, nodos 20%, tiempo 10%. Lo pusimos porque no ayuda a confirmar matematicamente si las interpretaciones están realmente fundamentadas.



## Lo que encontramos

El programa detecta automáticamente cuál métrica es engañosa según los datos reales de cada corrida. La lógica funciona así:

- Si todos los agentes tienen la misma tasa de éxito **y** los mismos pasos — la tasa de éxito sola no sirve para diferenciarlos, aunque el Score Compuesto sí muestra diferencias en nodos y tiempo.
- Si todos tienen la misma tasa de éxito pero caminos de largo distinto — la tasa de éxito empata cuando no debería, porque la calidad del camino sí varía.
- Si el agente con mejor tasa de éxito no es el que gana en Score Compuesto — optimizar solo éxito puede llevarte a elegir un agente que en realidad es peor en todo lo demás.

En la mayoría de las corridas la **tasa de éxito** resulta ser la métrica engañosa, porque los tres agentes llegan en porcentajes similares pero con caminos y eficiencia muy distintos. Greedy suele explorar menos nodos que BFS y A\*, lo que parece una ventaja, pero sus caminos son más largos porque no acumula el costo real del recorrido.


## Estado Actual y Limitaciones

**Estado actual:** el benchmark funciona completo. Corre los 25 laberintos en 3 fases, calcula el Score Compuesto, detecta la métrica engañosa automáticamente, guarda el CSV y genera una gráfica por fase más el resumen final.

**Limitaciones de esta entrega:**
- Solo se comparan tres agentes; no hay variantes del mismo algoritmo.
- El porcentaje de paredes es fijo (30%); no hay variación de dificultad entre laberintos del mismo tamaño.
- Los laberintos son relativamente pequeños (máximo 15×15).
- No hay interfaz gráfica para visualizar el recorrido paso a paso.


## Roadmap (Visión Futura)

Para el PP2 y el TI final planeamos:

- Variar el porcentaje de paredes (20%, 40%, 50%) para ver cómo aguantan los agentes ante distintas dificultades.
- Agregar laberintos mucho más grandes (tipo 100×100 o más) para observar cómo escala cada algoritmo.
- Agregar al menos uno o 2 agentes para ampliar la comparación.
- Evaluar si las conclusiones sobre métricas engañosas se mantienen cuando cambia el entorno.


## Uso de IA

Usamos Claude (Anthropic) para ayudarnos a ordenar y revisar el código. El diseño del benchmark, la selección de métricas y el análisis de resultados lo definimos nosotros.