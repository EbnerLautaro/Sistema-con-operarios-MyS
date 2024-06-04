import math
from typing import Callable
from aux import exponencial


def ejercicio_1(N: int, S: int, Tf: float, Tr: float) -> float:
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

    # Definimos los parametros de las variables exponenciales

    # Obtenemos los tiempos de fallos de las maquinas y ordenamos de menor a mayor
    tiempos_fallo = [exponencial(Tf) for _ in range(N)]
    tiempos_fallo.sort()

    # seteamos el tiempo de reparacion en infinito
    t_reparacion = math.inf

    # Inicializamos tanto el tiempo y la cantidad de maquinas defectuosas en 0
    t = 0
    cant_defectuosas = 0

    # Mientras el supermercado es operativo
    while cant_defectuosas <= S:

        # Si el proximo evento es un fallo de una maquina
        if tiempos_fallo[0] <= t_reparacion:
            # Avanzamos el tiempo hasta el fallo de la maquina
            t = tiempos_fallo[0]

            # Incrementamos en uno la cantidad de maquinas defectuosas
            cant_defectuosas += 1

            # Si el supermercado deja de ser operativo, retornamos el tiempo actual
            if cant_defectuosas > S:
                break
            # Si no estamos reparando ninguna maquina, creamos el evento de reparacion
            if t_reparacion == math.inf:
                # La maquina se terminara de reparar en en tiempo actual mas lo que lleve reparar la maquina
                t_reparacion = t + exponencial(Tr)

            # Actualizamos la lista de eventos de fallos, eliminando la maquina que acaba de fallar
            # y agregando una maquina
            tiempos_fallo = tiempos_fallo[1:]
            tiempos_fallo.append(t + exponencial(Tf))
            tiempos_fallo.sort()

        # el proximo evento es una reparacion
        else:
            # if tiempos_fallo[0] > t_reparacion:
            # arreglamos una maquina
            cant_defectuosas -= 1

            # Avanzamos el tiempo hasta la reparacion de la maquina
            t = t_reparacion

            # si hay alguna defectuosa, empiezo a reparar
            if cant_defectuosas >= 1:
                t_reparacion = t + exponencial(Tr)
            # si no hay ninguna defectuosa, dejo de reparar
            else:
                t_reparacion = math.inf
    return t


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
        return ejercicio_1(N=N, S=S, Tf=Tf, Tr=Tr)

    esperanza, varianza = calcular_metricas(
        sim=simulacion, n_sim=100_000
    )
    print("\n\nsimulacion_ebner\n\n")
    print(f"parametros \tTf={Tf} Tr={Tr}")
    print(f"Esperanza\t{esperanza}")
    print(f"Varianza \t{varianza}")
    print(f"Desviacion\t{math.sqrt(varianza)}")
