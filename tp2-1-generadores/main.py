import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import stats
from gcl_generator import generador_gcl
from mersenne_twister_generator import generador_mersenne_twister

# Parámetros
m = 2**32
a = 1664525
c = 1013904223
seed = 12345
n = 1000

# Generar números pseudoaleatorios
numeros_gcl = generador_gcl(m, a, c, seed, n)
numeros_mt = generador_mersenne_twister(seed, n)
numeros_python = [random.randint(0, 2**32 - 1) for _ in range(n)]

# Prueba de distribución uniforme
def prueba_distribucion_uniforme(numeros, nombre_generador):
    plt.hist(numeros, bins=50, color='blue', alpha=0.7)
    plt.title(f'Distribución Uniforme - {nombre_generador}')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.show()

# Prueba de media y varianza
def prueba_media_varianza(numeros, nombre_generador):
    media = np.mean(numeros)
    varianza = np.var(numeros)
    print(f'Media de los números generados por {nombre_generador}: {media}')
    print(f'Varianza de los números generados por {nombre_generador}: {varianza}')

# Prueba de chi-cuadrado
def prueba_chi_cuadrado(numeros, nombre_generador):
    frec_esperada = len(numeros) / 50  # Esperamos que haya 20 números en cada bin (50 bins)
    frec_observada, bins, _ = plt.hist(numeros, bins=50, color='blue', alpha=0.7)
    chi_cuadrado, p_valor = stats.chisquare(frec_observada, frec_esperada)
    print(f'Chi-cuadrado para {nombre_generador}: {chi_cuadrado}')
    print(f'p-valor para {nombre_generador}: {p_valor}')

# Realizar pruebas y graficar resultados
prueba_distribucion_uniforme(numeros_gcl, 'GCL')
prueba_media_varianza(numeros_gcl, 'GCL')
prueba_chi_cuadrado(numeros_gcl, 'GCL')

prueba_distribucion_uniforme(numeros_mt, 'Mersenne Twister')
prueba_media_varianza(numeros_mt, 'Mersenne Twister')
prueba_chi_cuadrado(numeros_mt, 'Mersenne Twister')

prueba_distribucion_uniforme(numeros_python, 'Python Random')
prueba_media_varianza(numeros_python, 'Python Random')
prueba_chi_cuadrado(numeros_python, 'Python Random')