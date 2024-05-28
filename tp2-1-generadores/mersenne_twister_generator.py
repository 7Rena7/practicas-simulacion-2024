import random

# Implementación del Generador de Mersenne Twister
def generador_mersenne_twister(seed, n):
    random.seed(seed)
    return [random.getrandbits(32) for _ in range(n)]

# Implementación del Generador de Mersenne Twister para números binarios
def generador_mersenne_twister_binario(seed, n):
    random.seed(seed)
    return [random.getrandbits(1) for _ in range(n)]
 