import math
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
    lamda_reparacion = 1/Tr
    lamda_fallo = 1/Tf

    # Obtenemos los tiempos de fallos de las maquinas y ordenamos de menor a mayor
    tiempos_fallo = [exponencial(lamda=lamda_fallo) for _ in range(N)]
    tiempos_fallo.sort()

    # Inicializamos el tiempo de reparacion en infinito, esto representa que no estamos reparando nada
    t_reparacion = math.inf

    # Inicializamos tanto el tiempo como la cantidad de maquinas defectuosas en 0
    t = 0
    cant_defectuosas = 0

    # Mientras el supermercado es operativo
    while cant_defectuosas <= S:

        # Si el proximo evento es un fallo de una maquina
        if tiempos_fallo[0] <= t_reparacion:

            t = tiempos_fallo[0]

            # Incrementamos en uno la cantidad de maquinas defectuosas
            cant_defectuosas += 1

            # si el supermercado deja de ser operativo
            if cant_defectuosas > S:
                return t

            # Si no estamos reparando ninguna
            if t_reparacion == math.inf:
                # definimos el tiempo en el cual terminamos de reparar una maquina
                t_reparacion = t + exponencial(lamda=lamda_reparacion)

            # Eliminamos el primero
            tiempos_fallo = tiempos_fallo[1:]
            # agreamos una maquina
            tiempos_fallo.append(t + exponencial(lamda=lamda_fallo))
            # Ordenamos de menor a mayor
            tiempos_fallo.sort()

        # el proximo evento es una reparacion
        if tiempos_fallo[0] >= t_reparacion:
            # arreglamos una maquina
            cant_defectuosas -= 1

            # si hay alguna defectuosa, empiezo a reparar
            if cant_defectuosas > 0:
                t_reparacion += exponencial(lamda_reparacion)
            # si no hay ninguna defectuosa, dejo de reparar
            else:
                t_reparacion = math.inf

    return t


if __name__ == '__main__':

    from main import ejercicio_1 as molina_1

    n_sim = 100_000

    suma_ebner = 0
    suma_molina = 0

    for _ in range(n_sim):
        suma_ebner += ejercicio_1(7, 3, 1, (1/8))
        suma_molina += molina_1(7, 3, 1, (1/8))
    print(f"Media ebner \t{suma_ebner/n_sim}")
    print(f"Media molina\t{suma_molina/n_sim}")
