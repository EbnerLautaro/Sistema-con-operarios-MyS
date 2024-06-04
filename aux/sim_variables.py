import random
import math
from typing import List, Tuple


def exponencial(lamda: float) -> float:
    """
    Simulacion de una variable aleatoria exponencial a travez del metodo de la inversa

    Args:
        lamda (float): tasa de intensidad.

    Returns:
        float: variable aleatoria exponencial.
    """
    u = 1 - random.random()
    return -math.log(u) / lamda


def proceso_poisson(lamda, T) -> Tuple[int, list[float]]:
    """
    Simulacion de un proceso de poisson homogeneo

    Args:
        lamda (float): tasa de intensidad.
        T (float): tiempo maximo.

    Returns:
        int: cantidad de eventos.
        list: lista de eventos.
    """
    t = 0
    events: List[float] = []
    while t < T:
        u = random.random()
        t += exponencial(lamda=lamda)
        if t <= T:
            events.append(t)
    return len(events), events
