**EIF420-O · Inteligencia Artificial**
# ProyectoIA — G2 - Evaluación de agentes cómo medir inteligencia sin autoengañarse

---

## PP1

Para el PP1 del curso implementamos un benchmark para comparar tres agentes resolviendo laberintos: BFS, A* y Greedy. La idea no era ver quién llega más, sino entender si las métricas que usamos para medir eso realmente dicen lo que creemos que dicen.


## Lo Necesario

Se necesita Python 3.8+ y matplotlib:

```bash
pip install matplotlib
python main.py
```


## ¿Que hace?

El programa corre en tres fases (5x5, 10x10, 15x15) y va pidiendo que presiones Enter entre cada una. Al final guarda los resultados en un CSV y genera las gráficas.


## Archivos

```
main.py       → corre todo el benchmark por fases
agentes.py    → implementación de BFS, A* y Greedy
benchmark.py  → genera los 25 laberintos con semilla fija
metricas.py   → mide tiempo, pasos, nodos y éxito
```


## ¿Qué comparamos?

Tres algoritmos de búsqueda sobre laberintos generados aleatoriamente:

- **BFS** — busca nivel por nivel, siempre encuentra el camino más corto
- **A\*** — usa heurística Manhattan más el costo acumulado, también óptimo
- **Greedy** — solo mira qué tan cerca está de la meta, rápido pero no óptimo

Los laberintos son 25 en total: 10 de 5x5, 10 de 10x10 y 5 de 15x15. Todos generados con semillas fijas para que sean reproducibles.


## Métricas

Medimos cuatro cosas por cada ejecución:

- **Tasa de éxito** — ¿llegó a la meta?
- **Pasos** — qué tan largo fue el camino
- **Tiempo (ms)** — cuánto tardó
- **Nodos explorados** — cuántas celdas revisó antes de llegar

También calculamos un **Score Compuesto (0–100)** que combina las cuatro con pesos: éxito 40%, pasos 30%, nodos 20%, tiempo 10%. Lo pusimos porque si no, es difícil decir quién ganó cuando cada agente gana en una métrica distinta.


## Lo que encontramos

Al final de cada corrida el sistema analiza los datos reales y detecta automáticamente cuál métrica está siendo engañosa en ese benchmark. La lógica que pusimos funciona así:

- Si todos los agentes tienen la misma tasa de éxito y los mismos pasos — la tasa de éxito sola no sirve para diferenciarlos, aunque el Score Compuesto sí muestra diferencias en nodos y tiempo.

- Si todos tienen la misma tasa de éxito pero caminos de largo distinto — la tasa de éxito empata cuando no debería, porque la calidad del camino sí varía.

- Si el agente con mejor tasa de éxito no es el que gana en Score Compuesto — optimizar solo éxito puede llevarte a elegir un agente que en realidad es peor en todo lo demás.

En la mayoría de las corridas la tasa de éxito es la métrica engañosa, porque los tres agentes llegan en porcentajes similares pero con caminos y eficiencia muy distintos. Greedy suele explorar menos nodos que BFS y A*, lo que parece una ventaja, pero sus caminos son más largos porque no acumula costo real.


## Qué falta para el PP2

- Agregar 1 o 2 agentes más
- Variar el porcentaje de paredes (probar con 20%, 40%, 50%) para ver cómo aguantan los agentes
- Crear uno o varios laberintos mucho más grandes. (tipo 500x500)
- Agregar algún tipo de perturbación durante la ejecución
- Ver si el Score Compuesto se mantiene consistente cuando cambia el entorno


## Uso de IA

Usamos Claude (Anthropic) para ayudarnos a odernar, optimizar el código y revisar la fórmula del Score Compuesto. El desarrollo y diseño del benchmark, las métricas y el análisis de resultados lo definimos nosotros.
