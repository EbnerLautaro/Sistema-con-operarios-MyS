import math
from aux import exponencial


def ejercicio_1(N: int, S: int, Tf: float, Tr: float) -> float:
    lamda_fallo = Tf
    lamda_reparacion = Tr

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


def ejercicio_2(N: int, S: int, Tf: float, Tr: float) -> float:
    lamda_fallo = Tf
    lamda_reparacion = Tr

    tiempos_fallo = sorted([exponencial(lamda=lamda_fallo) for _ in range(N)])
    maquinas_repuesto = S
    prox_rep1 = math.inf
    prox_rep2 = math.inf

    while (maquinas_repuesto > 0) or (tiempos_fallo[0] >= prox_rep1) or (tiempos_fallo[0] >= prox_rep2):

        # si termine de reparar una maquina, avanzo el tiempo hasta que pueda reparar alguna
        if tiempos_fallo[0] <= prox_rep1 and tiempos_fallo[0] <= prox_rep2:

            # se rompio una maquina
            maquinas_repuesto -= 1
            t = tiempos_fallo[0]

            # Si es la primera reparacion
            if prox_rep1 == math.inf:
                prox_rep1 = t + exponencial(lamda=lamda_reparacion)
            elif prox_rep2 == math.inf:
                prox_rep2 = t + exponencial(lamda=lamda_reparacion)

            # Eliminamos el primero
            # Agregamos cuando se rompe la nueva y sorteamos
            tiempos_fallo = tiempos_fallo[1:]
            tiempos_fallo.append(t + exponencial(lamda=lamda_fallo))
            tiempos_fallo = sorted(tiempos_fallo)

        elif tiempos_fallo[0] >= prox_rep1 and prox_rep2 >= prox_rep1:  # reparacion
            maquinas_repuesto += 1
            if maquinas_repuesto < S:  # si no tengo todos los repuestos ok
                prox_rep1 = prox_rep1 + \
                    exponencial(lamda=lamda_reparacion)
            else:
                prox_rep1 = math.inf

        elif tiempos_fallo[0] >= prox_rep2 and prox_rep1 >= prox_rep2:
            maquinas_repuesto += 1
            if maquinas_repuesto < S:  # si no tengo todos los repuestos ok
                prox_rep2 = prox_rep2 + \
                    exponencial(lamda=lamda_reparacion)
            else:
                prox_rep2 = math.inf

    return tiempos_fallo[0]


if __name__ == '__main__':
    from aux import calcular_metricas

    def sim():
        return ejercicio_2(7, 3, 1, 8)

    esperanza, varianza = calcular_metricas(
        sim=sim, n_sim=10000
    )
    print("\n\nsimulacion_2_operarios - molina\n\n")
    print(f"Esperanza\t{esperanza}")
    print(f"Varianza \t{varianza}")
    print(f"Desviacion\t{math.sqrt(varianza)}")
