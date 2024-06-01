import random, math


def exponencial(lamda):
    u = random.random()
    return -math.log(u) / lamda
