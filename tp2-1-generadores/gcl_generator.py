# Implementación del Generador Congruencial Lineal (GCL)
def generador_gcl(m, a, c, seed, n):
    numeros = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x)
    return numeros