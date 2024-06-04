import random
import math
from typing import Callable


def simulacion_ross(N: int, S: int, Tf: float, Tr: float) -> float:
    """
    Simula el tiempo hasta el fallo del sistema del supermercado.

    Args:
        - N (int): número de cajas registradoras en servicio.
        - S (int): número de máquinas de repuesto.
        - Tf (float): tiempo medio hasta que una caja falla.
        - Tr (float): tiempo medio de reparación de una caja.

    Returns:
        - float: tiempo hasta que el sistema falla.
    """

    # INITIALIZE
    t: float = 0
    cant_defectuosas: int = 0  # la cantidad de maquinas defectuosas al tiempo t
    t_reparacion: float = math.inf

    fallos = [random.expovariate(Tf) for _ in range(N)]
    fallos.sort()

    while True:

        # Ocurre un fallo antes de una reparacion
        if fallos[0] < t_reparacion:
            # adelantamos el tiempo hasta el fallo de la maquina
            t = fallos[0]

            cant_defectuosas = cant_defectuosas + 1

            # falla una maquina pero sigue operativo
            if cant_defectuosas < S + 1:
                # eliminamos la maquina y agregamos otra
                fallos = fallos[1:]
                fallos.append(t + random.expovariate(Tf))
                fallos.sort()

            # solo fallo una maquina, iniciamos el arreglo
            if cant_defectuosas == 1:
                t_reparacion = t + random.expovariate(Tr)

            # el supermercado deja de ser operativo
            if cant_defectuosas > S:
                return t

        # ocurre una reparacion antes de un fallo
        else:

            cant_defectuosas = cant_defectuosas - 1

            # adelantamos el tiempo hasta que termine la reparacion
            t = t_reparacion

            # si hay para reparar, empezamos a reparar
            if cant_defectuosas > 0:
                t_reparacion = t + random.expovariate(Tr)

            # dejamos de reparar
            else:
                t_reparacion = math.inf


def calcular_metricas(sim: Callable, n_sim: int = 100_000):
    suma = 0
    suma_cuadrada = 0

    for _ in range(n_sim):
        res = sim()
        suma += res
        suma_cuadrada += res**2

    mean = suma/n_sim
    variance = (suma_cuadrada/n_sim) - (mean**2)
    return mean, variance


if __name__ == '__main__':

    N = 7
    S = 3
    Tf = 1
    Tr = 8

    def simulacion():
        return simulacion_ross(N=N, S=S, Tf=Tf, Tr=Tr)

    esperanza, varianza = calcular_metricas(
        sim=simulacion, n_sim=100_000
    )
    print("\n\nsimulacion_ross\n\n")
    print(f"parametros \tTf={Tf} Tr={Tr}")
    print(f"Esperanza\t{esperanza}")
    print(f"Varianza \t{varianza}")
    print(f"Desviacion\t{math.sqrt(varianza)}")
