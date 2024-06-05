# Reporte - Sistema con operarios - A Repair problem

### Integrantes
- [Ebner Lautaro](lautaro.ebner@mi.unc.edu.ar)
- [Molina Franco](franco.molina13@mi.unc.edu.ar)

## Introduccion
### Presentacion del problema
En este informe, abordamos la simulación de un modelo de reparación para un pequeño supermercado que cuenta con $N$ cajas registradoras en servicio y un conjunto de $S$ máquinas de repuesto. 
Las cajas registradoras son susceptibles a fallos y requieren reparación. 
El objetivo de este estudio es determinar el tiempo medio y la desviación estándar del tiempo hasta que el supermercado deje de ser operativo, es decir, cuando hay más de $S$ cajas registradoras en reparacion o defectuosas.

Para poder estudiar este problema, simularemos dos casos muy distinguidos:
1. **Simulación con un operario:** Aquí, modelamos el proceso de fallo y reparación de las cajas registradoras utilizando un operario. El operario repara una máquina a la vez, y los tiempos de fallo y reparación se modelan como variables aleatorias exponenciales con parámetros $T_{F}$ (tiempo medio hasta fallar) y $T_{R}$ (tiempo medio de reparación), respectivamente.
2. **Simulación con dos operarios:** En esta segunda parte, extendemos el modelo anterior para incluir dos operarios que trabajan en paralelo entre ellos. Cada operario puede reparar una máquina a la vez, lo que potencialmente reduce el tiempo total de reparación y aumenta el tiempo medio hasta el fallo del sistema.

### Procedimiento de Simulación
Para simular el modelo de reparación de las cajas registradoras, seguimos estos pasos:

1. **Definición de parámetros**:
    - $N$: Número de cajas registradoras en servicio.
    - $S$: Número de máquinas de repuesto.
    - $T_{F}$: Tiempo medio hasta que una caja registradora falla.
    - $T_{R}$: Tiempo medio de reparación de una caja registradora.
2. **Generación de tiempos de fallo y reparación**:
    - Utilizamos la distribución exponencial para modelar los tiempos de fallo y reparación.
    - El tiempo hasta que una caja registradora falla se genera como una variable aleatoria exponencial con media $T_{F}$.
    - El tiempo de reparación de una caja se genera como una variable aleatoria exponencial con media $T_{R}$.
3. **Simulación del proceso**:
    - Iniciamos con todas las cajas registradoras en funcionamiento.
    - Registramos los tiempos de fallo y reparamos las cajas de acuerdo con la disponibilidad del operario o de los dos operarios.
    - Mantenemos un registro de cuántas cajas están en reparacion o defectuosas y cuántas están operativas en cada momento.
    - La simulación se detiene cuando el número de cajas operativas cae por debajo de $N$, es decir, cuando más de $S$ cajas están en reparación o defectuosas.
4. **Cálculo del tiempo medio y la desviación estándar**:
   - Repetimos la simulación múltiples veces para obtener una distribución del tiempo hasta el fallo del sistema.
   - Calculamos el tiempo medio y la desviación estándar de esta distribución.
  
Este enfoque nos permitirá no solo entender el comportamiento del sistema bajo diferentes condiciones, sino también tomar decisiones informadas sobre cómo mejorar la operatividad del supermercado.

## Algoritmo y descripcion de las variables

Como ya mencionamos antes, las variables o parametros de la simulacion utilizados fueron:

  - $N$: Número de cajas registradoras en servicio.
  - $S$: Número de máquinas de repuesto.
  - $T_{F}$: Tiempo medio hasta que una caja registradora falla.
  - $T_{R}$: Tiempo medio de reparación de una caja registradora.

A continuacion daremos una simple explicacion de cada uno de los algoritmos planteados.

### **Sistema con un operario**

   1. Inicializa el tiempo (t) como 0, el número de máquinas defectuosas en el tiempo t como 0 y el tiempo de reparación (t_reparacion) como infinito.
   2. Genera una lista de fallos de las cajas registradoras utilizando una distribución exponencial con una tasa promedio de fallos (Tf). La lista está ordenada de menor a mayor tiempo de fallo.
   3. En un bucle infinito, el algoritmo evalúa continuamente si ocurre un fallo antes de que termine una reparación o si una reparación ocurre antes de que ocurra un fallo.
   4. Si ocurre un fallo antes de una reparación, actualiza el tiempo (t) al tiempo del fallo y aumenta la cantidad de máquinas defectuosas.
      - Si hay menos máquinas defectuosas que máquinas de repuesto más una (S+1), se elimina la máquina defectuosa y se agrega una nueva con un tiempo de fallo calculado.
      - Si solo falla una máquina, se programa su reparación.
      - Si la cantidad de máquinas defectuosas supera el límite de repuestos (S), el algoritmo devuelve el tiempo actual (t) indicando que el sistema ha fallado.
   5. Si ocurre una reparación antes de un fallo, disminuye la cantidad de máquinas defectuosas, actualiza el tiempo (t) al tiempo de finalización de la reparación y, si hay más máquinas para reparar, programa la siguiente reparación.
   6. El algoritmo continúa ejecutándose hasta que se alcanza un punto donde el sistema falla o hasta que se detiene la simulación. En cualquier caso, devuelve el tiempo en el que ocurrió el fallo del sistema.

