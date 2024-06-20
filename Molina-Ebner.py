import random
import math
from typing import Callable, List
import matplotlib.pyplot as plt


def make_graphs(sims: List[Callable], n_sim: int = 10_000):

    data = []
    means = []
    vars = []
    deviations = []
    for sim in sims:
        data_sim = []
        suma = 0
        suma_cuadrada = 0
        for _ in range(n_sim):
            x = sim()
            suma += x
            suma_cuadrada += x**2
            data_sim.append(x)

        mean = suma / n_sim
        var = (suma_cuadrada / n_sim) - (mean**2)

        means.append(mean)
        vars.append(var)
        deviations.append(math.sqrt(var))
        data.append(data_sim)

    plt.hist(
        x=data,
        bins=[0] + [i / 2 for i in range(30)],
        label=[sim.__name__ for sim in sims],
    )
    plt.xticks([0] + [i / 2 for i in range(30)])

    plt.xlabel("Tiempo")
    plt.ylabel("Frecuencia")
    plt.title("Histogramas de tiempos")
    plt.legend()
    plt.show()

    def create_bar_chart(x_labels, values, title, ylabel, color):
        fig, ax = plt.subplots(figsize=(10, 4))
        bars = ax.bar(x_labels, values, color=color, alpha=0.7)
        ax.set_title(title)
        ax.set_ylabel(ylabel)

        for bar in bars:
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                round(yval, 2),
                ha="center",
                va="bottom",
            )

        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels)

        plt.tight_layout()
        plt.show()

    x_labels = [sim.__name__ for sim in sims]

    create_bar_chart(x_labels, means, "Medias muestrales", "Media", "blue")
    create_bar_chart(
        x_labels, deviations, "Desviaciones Estándar", "Desviación Estándar", "red"
    )


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

            cant_en_reparacion = len([x for x in t_reparacion if x != math.inf])

            # cantidad de maquinas que no estan siendo trabajadas
            cant_reparables = cant_defectuosas - cant_en_reparacion

            # si hay para reparar, empezamos a reparar
            if cant_reparables > 0:
                t_reparacion[index] = t + random.expovariate(Tr)

            # dejamos de reparar
            else:
                t_reparacion[index] = math.inf


if __name__ == "__main__":

    def Escenario_A():
        return simulacion_M_operarios(N=7, S=3, Tf=1, Tr=8, M=1)

    def Escenario_B():
        return simulacion_M_operarios(N=7, S=3, Tf=1, Tr=8, M=2)

    def Escenario_C():
        return simulacion_M_operarios(N=7, S=4, Tf=1, Tr=8, M=1)

    make_graphs(
        sims=[Escenario_A, Escenario_B, Escenario_C],
        n_sim=10_000,
    )

    # for sim in [simulacionA, simulacionB, simulacionC]:

    #     print(f"\n{sim.__name__}".center(10, "-"))

    #     esperanza_sim, varianza_sim = calcular_metricas(sim=sim, n_sim=10_000)

    #     print(f"Esperanza: \t{esperanza_sim:.4f}")
    #     print(f"Varianza \t{varianza_sim:.4f}")
    #     print(f"Desviacion\t{math.sqrt(varianza_sim):.4f}")
