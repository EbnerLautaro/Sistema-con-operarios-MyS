import random
import math
from typing import Callable
from aux import calcular_metricas


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


def simulacion_2_operarios(N: int, S: int, Tf: float, Tr: float) -> float:
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

    t: float = 0
    cant_defectuosas: int = 0  # la cantidad de maquinas defectuosas al tiempo t
    t_reparacion_o1: float = math.inf
    t_reparacion_o2: float = math.inf

    fallos = [random.expovariate(Tf) for _ in range(N)]
    fallos.sort()

    while True:

        # Ocurre un fallo antes de una reparacion
        if min([fallos[0], t_reparacion_o1, t_reparacion_o2]) == fallos[0]:
            # adelantamos el tiempo hasta el fallo de la maquina
            t = fallos[0]

            cant_defectuosas = cant_defectuosas + 1

            # falla una maquina pero sigue operativo
            if cant_defectuosas < S + 1:
                # eliminamos la maquina y agregamos otra
                fallos = fallos[1:]
                fallos.append(t + random.expovariate(Tf))
                fallos.sort()

            # si algun operario esta al pedo, que labure
            if t_reparacion_o1 == math.inf:
                t_reparacion_o1 = t + random.expovariate(Tr)
            elif t_reparacion_o2 == math.inf:
                t_reparacion_o2 = t + random.expovariate(Tr)

            # el supermercado deja de ser operativo
            if cant_defectuosas > S:
                return t

        # si el proximo evento es el fin del operario 1
        elif min([fallos[0], t_reparacion_o1, t_reparacion_o2]) == t_reparacion_o1:
            # elif fallos[0] >= t_reparacion_o1 and t_reparacion_o1 <= t_reparacion_o2:
            cant_defectuosas = cant_defectuosas - 1

            # adelantamos el tiempo hasta que termine la reparacion
            t = t_reparacion_o1

            # si hay para reparar, empezamos a reparar
            if cant_defectuosas > 0:
                t_reparacion_o1 = t + random.expovariate(Tr)

            # dejamos de reparar
            else:
                t_reparacion_o1 = math.inf

        # si el proximo evento es el fin del operario 2
        # elif fallos[0] >= t_reparacion_o2 and t_reparacion_o2 <= t_reparacion_o1:
        elif min([fallos[0], t_reparacion_o1, t_reparacion_o2]) == t_reparacion_o2:

            cant_defectuosas = cant_defectuosas - 1

            # adelantamos el tiempo hasta que termine la reparacion
            t = t_reparacion_o2

            # si hay para reparar, empezamos a reparar
            if cant_defectuosas > 0:
                t_reparacion_o2 = t + random.expovariate(Tr)

            # dejamos de reparar
            else:
                t_reparacion_o2 = math.inf


def simulacion_M_operarios(N: int, S: int, Tf: float, Tr: float, M: int) -> float:
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

    t: float = 0
    cant_defectuosas: int = 0  # la cantidad de maquinas defectuosas al tiempo t

    t_reparacion: list[float] = [math.inf for _ in range(M)]
    fallos = [random.expovariate(Tf) for _ in range(N)]
    fallos.sort()

    while True:

        # Ocurre un fallo antes de una reparacion
        if min(t_reparacion) > fallos[0]:
            # adelantamos el tiempo hasta el fallo de la maquina
            t = fallos[0]

            cant_defectuosas = cant_defectuosas + 1

            # falla una maquina pero sigue operativo
            if cant_defectuosas < S + 1:
                # eliminamos la maquina y agregamos otra
                fallos = fallos[1:]
                fallos.append(t + random.expovariate(Tf))
                fallos.sort()

            # si algun operario esta al pedo, que labure
            if math.inf in t_reparacion:
                index = t_reparacion.index(math.inf)
                t_reparacion[index] = t + random.expovariate(Tr)

            # el supermercado deja de ser operativo
            if cant_defectuosas > S:
                return t

        elif min(t_reparacion) <= fallos[0]:

            # adelantamos el tiempo hasta que termine la reparacion
            index = t_reparacion.index(min(t_reparacion))
            t = t_reparacion[index]
            t_reparacion[index] = math.inf
            cant_defectuosas = cant_defectuosas - 1

            cant_en_reparacion = len(
                [x for x in t_reparacion if x != math.inf]
            )

            # cantidad de maquinas que no estan siendo trabajadas
            cant_reparables = cant_defectuosas - cant_en_reparacion

            # si hay para reparar, empezamos a reparar
            if cant_reparables > 0:
                t_reparacion[index] = t + random.expovariate(Tr)

            # dejamos de reparar
            else:
                t_reparacion[index] = math.inf


if __name__ == '__main__':

    N = 7
    S = 3
    Tf = 1
    Tr = 8
    M = 2

    def simulacion():
        return simulacion_M_operarios(N=N, S=S, Tf=Tf, Tr=Tr, M=M)

    esperanza, varianza = calcular_metricas(
        sim=simulacion, n_sim=10_000
    )
    print(f"\nsimulacion_M_operarios(N={N}, S={S}, Tf={Tf}, Tr={Tr}, M={M})\n")
    print(f"Esperanza\t{esperanza:.4f}")
    print(f"Varianza \t{varianza:.4f}")
    print(f"Desviacion\t{math.sqrt(varianza):.4f}")
