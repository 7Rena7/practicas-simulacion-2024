import matplotlib.pyplot as plt
import numpy as np
import random
from math import log2
import pandas as pd
from scipy import stats

from gcl_generator import generador_gcl
from mersenne_twister_generator import generador_mersenne_twister 

# Parámetros
m = 2**32 # Módulo
a = 1664525 # Multiplicador
c = 1013904223 # Incremento
seed = 12345 # Semilla
n = 512 ** 2 # Cantidad de números a generar
 
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
    plt.savefig(f'./images/distribucion_{nombre_generador}.png')
    plt.show()

# Prueba de media y varianza
def prueba_media_varianza(numeros, nombre_generador):
    media = np.mean(numeros)
    varianza = np.var(numeros)
    print(f'Media de los números generados por {nombre_generador}: {media}')
    print(f'Varianza de los números generados por {nombre_generador}: {varianza}')


def prueba_chi_cuadrado(numeros, nombre_generador):
    # Esperamos que haya una frecuencia esperada en cada bin
    subintervalos =  int(1 + log2(len(numeros))) # para 512^2 = 262144
    frec_esperada = len(numeros) / subintervalos
    # Generar histograma y obtener la frecuencia observada
    frec_observada, bins, _ = plt.hist(numeros, bins=subintervalos, color='blue', alpha=0.7, edgecolor='black')
    
    # Calcular chi-cuadrado
    chi_cuadrado, p_valor = stats.chisquare(frec_observada, [frec_esperada]*len(frec_observada))
    print(f'Chi-cuadrado para {nombre_generador}: {chi_cuadrado}')
    print(f'Frecuencia observada para {nombre_generador}: {sum(frec_observada)/len(frec_observada)} vs {frec_esperada}')
    print(f'p-valor para {nombre_generador}: {p_valor}')
    
    # Añadir títulos y etiquetas
    plt.title(f'Histograma de {nombre_generador}')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    
    # Guardar la gráfica
    plt.savefig(f'./images/histograma_{nombre_generador}.png')
    plt.show()
    
    return chi_cuadrado, p_valor