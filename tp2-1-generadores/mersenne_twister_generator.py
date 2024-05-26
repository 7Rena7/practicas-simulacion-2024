import random

# Implementación del Generador de Mersenne Twister
def generador_mersenne_twister(seed, n):
    random.seed(seed)
    return [random.getrandbits(32) for _ in range(n)]