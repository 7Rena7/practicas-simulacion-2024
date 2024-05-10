import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sys import argv as arguments, exit
from os import path as filepath
from martingala import Martingala

# Verificar si se proporciona el número correcto de argumentos en la línea de comandos. Se deben proporcionar ocho
# argumentos: -c <num_tiradas> -n <num_corridas> -e <numero_elegido> -s <estrategia> -a <tipo_capital>.
# Se debe cumplir:
#   -c y -n deben ser enteros mayores a cero
#   -e debe estar entre 0 y 36
#   -s es la estrategia utilizada, puede ser m (Martingale), d (D’Alambert), f (Fibonacci) u p (Paroli)
#   -a es el tipo de capital, puede ser: f (fijo) o i (infinito)
print("Cantidad de argumentos: {}".format(len(arguments)))
print("Argumentos: {}".format(arguments))

if len(arguments) != 11 or arguments[1] != "-c" or arguments[3] != "-n" or arguments[5] != "-e" or arguments[7] != "-s" or arguments[9] != "-a":
    print("La cantidad de argumentos o su orden es incorrecta.\n")
    print("Uso: python/python3 {} -c <cantidad_de_tiradas>[int 1-1000] -n <cantidad_de_corridas>[int 1-100] -e "
          "<numero_elegido>[int 0-36] -s <estrategia>[m, d, f, p] -a <tipo_capital>[f, i]\n".format(filepath.basename(__file__)))
    print("Las estraegias pueden ser: m (Martingale), d (D'Alambert), f (Fibonacci) u p (Paroli)")
    print("El tipo de capital puede ser: f (fijo) o i (infinito)")
    print("Ejemplo: python/python3 {} -c 1000 -n 10 -e 8 -s m -a f".format(filepath.basename(__file__)))
    exit(1)

# Obtener el número de tiradas, corridas, el número seleccionado, la estrategia y el tipo de capital de los argumentos de la línea de comandos
cantidad_tiradas = int(arguments[2])
cantidad_corridas = int(arguments[4])
numero_elegido = int(arguments[6])
estrategia = arguments[8]
tipo_capital = arguments[10]

if (cantidad_tiradas < 1):
    print("El número de tiradas debe ser mayor a 0.")
    exit(1)

if (cantidad_corridas < 1):
    print("El número de corridas debe ser mayor a 0.")
    exit(1)

if not (0 <= numero_elegido <= 36):
    print("El número elegido debe estar entre 0 y 36.")
    exit(1)

if not (estrategia in ['m', 'd', 'f', 'p']):
    print("La estrategia debe ser m, d, f o p.")
    print("Las estraegias pueden ser: m (Martingale), d (D'Alambert), f (Fibonacci) u p (Paroli)")
    exit(1)

if not (tipo_capital in ['f', 'i']):
    print("El tipo de capital debe ser f o i.")
    print("El tipo de capital puede ser: f (fijo) o i (infinito)")
    exit(1)

print("***** Simulación de una Ruleta ***** \n"
      "Número de Tiradas: {} \n"
      "Número de Corridas: {} \n"
      "Número Elegido: {} \n"
      "Estrategia: {} \n"
      "Tipo de Capital: {} \n"
      .format(cantidad_tiradas, cantidad_corridas, numero_elegido, estrategia, tipo_capital))

if estrategia == 'm':
    martingale = Martingala(
        cantidad_tiradas, cantidad_corridas, numero_elegido, tipo_capital)
    martingale.ejecutar_estrategia()
    pass
elif estrategia == 'd':
    pass
elif estrategia == 'f':
    pass
else:
    pass