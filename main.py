import math
from aux import exponencial


def ejercicio_1(N: int, S: int, Tf: float, Tr: float) -> float:
    lamda_fallo = 1 / Tf
    lamda_reparacion = 1/Tr

    tiempos_fallo = sorted([exponencial(lamda=lamda_fallo) for _ in range(N)])
    maquinas_repuesto = S
    proxima_reparacion = math.inf

    while (maquinas_repuesto > 0) or (tiempos_fallo[0] >= proxima_reparacion):

        # si termine de reparar una maquina, avanzo el tiempo hasta que pueda reparar alguna
        if tiempos_fallo[0] <= proxima_reparacion:

            # se rompio una maquina
            maquinas_repuesto -= 1
            t = tiempos_fallo[0]

            # Si es la primera reparacion
            if proxima_reparacion == math.inf:
                proxima_reparacion = t + exponencial(lamda=lamda_reparacion)

            # Eliminamos el primero
            # Agregamos cuando se rompe la nueva y sorteamos
            tiempos_fallo = tiempos_fallo[1:]
            tiempos_fallo.append(t + exponencial(lamda=lamda_fallo))
            tiempos_fallo = sorted(tiempos_fallo)

        if tiempos_fallo[0] >= proxima_reparacion:  # reparacion
            maquinas_repuesto += 1
            if maquinas_repuesto < S:  # si no tengo todos los repuestos ok
                proxima_reparacion = proxima_reparacion + \
                    exponencial(lamda=lamda_reparacion)
            else:
                proxima_reparacion = math.inf

    return tiempos_fallo[0]


if __name__ == '__main__':
    N_i = 100_000
    suma = 0
    for _ in range(N_i):
        suma += ejercicio_1(7, 3, 1, (1/8))
    print(suma/N_i)
