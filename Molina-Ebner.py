import random
import math
from typing import Callable


def calcular_metricas(sim: Callable, n_sim: int = 100_000):
    suma = 0
    suma_cuadrada = 0

    for _ in range(n_sim):
        res = sim()
        suma += res
        suma_cuadrada += res**2

    media = suma / n_sim
    varianza = (suma_cuadrada / n_sim) - (media**2)
    return media, varianza


def simulacion_1_operario(N: int, S: int, Tf: float, Tr: float) -> float:

    t: float = 0
    # la cantidad de maquinas defectuosas al tiempo t
    cant_defectuosas: int = 0
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
            if t_reparacion == math.inf:
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


def simulacion_M_operarios(N: int, S: int, Tf: float, Tr: float, M: int) -> float:

    t: float = 0
    cant_defectuosas: int = 0  # la cantidad de maquinas defectuosas al tiempo t

    t_reparacion = [math.inf for _ in range(M)]
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
                [x for x in t_reparacion if x != math.inf])

            # cantidad de maquinas que no estan siendo trabajadas
            cant_reparables = cant_defectuosas - cant_en_reparacion

            # si hay para reparar, empezamos a reparar
            if cant_reparables > 0:
                t_reparacion[index] = t + random.expovariate(Tr)

            # dejamos de reparar
            else:
                t_reparacion[index] = math.inf


if __name__ == "__main__":

    def simulacionA():
        return simulacion_M_operarios(N=7, S=3, Tf=1, Tr=8, M=1)

    def simulacionB():
        return simulacion_M_operarios(N=7, S=3, Tf=1, Tr=8, M=2)

    def simulacionC():
        return simulacion_M_operarios(N=7, S=4, Tf=1, Tr=8, M=1)

    for sim in [simulacionA, simulacionB, simulacionC]:

        print(f'\n{sim.__name__}'.center(10, '-'))

        esperanza_sim, varianza_sim = calcular_metricas(
            sim=sim, n_sim=10_000)

        print(f"Esperanza: \t{esperanza_sim:.4f}")
        print(f"Varianza \t{varianza_sim:.4f}")
        print(f"Desviacion\t{math.sqrt(varianza_sim):.4f}")
