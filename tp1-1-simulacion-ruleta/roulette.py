import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sys import argv as arguments, exit
from os import path as filepath

# Verificar si se proporciona el número correcto de argumentos en la línea de comandos. Se deben proporcionar seis
# argumentos: -c <num_tiradas> -n <num_corridas> -e <numero_elegido>. -c y -n deben ser enteros mayores a cero y -e debe estar entre 0 y 36
if len(arguments) != 7 or arguments[1] != "-c" or arguments[3] != "-n" or arguments[5] != "-e":
    print("La cantidad de argumentos o su orden es incorrecta.\n")
    print("Uso: python/python3 {} -c <cantidad_de_tiradas>[int 1-1000] -n <cantidad_de_corridas>[int 1-100] -e "
          "<numero_elegido>[int 0-36]\n".format(filepath.basename(__file__)))
    print("Ejemplo: python/python3 {} -c 1000 -n 10 -e 8".format(filepath.basename(__file__)))
    exit(1)

# Obtener el número de tiradas, corridas y el número seleccionado de los argumentos de la línea de comandos
cantidad_tiradas = int(arguments[2])
cantidad_corridas = int(arguments[4])
numero_elegido = int(arguments[6])

if (cantidad_tiradas < 1):
    print("El número de tiradas debe ser mayor a 0.")
    exit(1)

if (cantidad_corridas < 1):
    print("El número de corridas debe ser mayor a 0.")
    exit(1)

if not (0 <= numero_elegido <= 36):
    print("El número elegido debe estar entre 0 y 36.")
    exit(1)

print("***** Simulación de una Ruleta ***** \n"
      "Número de Tiradas: {} \n"
      "Número de Corridas: {} \n"
      "Número Elegido: {} \n"
      .format(cantidad_tiradas, cantidad_corridas, numero_elegido))

desviacion_estandar_esperada = np.arange(0, 37, 1).std()
varianza_esperada = np.arange(0, 37, 1).var()
esperanza_matematica_esperada = np.arange(0, 37, 1).mean()


def graficar_frecuencia(frecuencia_relativa_listado, es_promedio):
    fig, ax = plt.subplots()

    ax.set_ylabel('fr (frecuencia relativa)')
    ax.set_xlabel('n (numero tiradas)')

    for frecuencia_relativa in frecuencia_relativa_listado:
        ax.plot([i for i in range(cantidad_tiradas)], frecuencia_relativa, linewidth=2.0, )

    ax.axhline(y=1 / 37, color='r', linestyle='--', label='frn (frecuencia relativa esperada)')

    ax.legend()

    if es_promedio:
        ax.set_title(f"FRECUENCIA RELATIVA DEL NUMERO {numero_elegido} PROMEDIO {cantidad_corridas} CORRIDAS")
    else:
        ax.set_title(f"FRECUENCIA RELATIVA DEL NUMERO {numero_elegido} {cantidad_corridas} CORRIDAS")

    plt.show()


def graficar_varianza(varianza_listado, es_promedio):
    fig, ax = plt.subplots()

    ax.set_ylabel('vv (valor de la varianza)')
    ax.set_xlabel('n (numero tiradas)')

    for varianza in varianza_listado:
        ax.plot([i for i in range(cantidad_tiradas)], varianza, linewidth=2.0, )

    ax.axhline(y=varianza_esperada, color='r', linestyle='--', label='vve (valor de la varianza esperada)')

    ax.legend()

    if es_promedio:
        ax.set_title(f"VARIANZA PROMEDIO {cantidad_corridas} CORRIDAS")
    else:
        ax.set_title(f"VARIANZA {cantidad_corridas} CORRIDAS")

    plt.show()


def graficar_desvio(desviacion_estandar_listado, es_promedio):
    fig, ax = plt.subplots()

    ax.set_ylabel('vd (valor del desvio)')
    ax.set_xlabel('n (numero tiradas)')

    for desviacion_estandar in desviacion_estandar_listado:
        ax.plot([i for i in range(cantidad_tiradas)], desviacion_estandar, linewidth=2.0, )

    ax.axhline(y=desviacion_estandar_esperada, color='r', linestyle='--', label='vde (valor del desvio esperado)')

    ax.legend()

    if es_promedio:
        ax.set_title(f"DESVÍO ESTANDAR PROMEDIO {cantidad_corridas} CORRIDAS")
    else:
        ax.set_title(f"DESVÍO ESTANDAR {cantidad_corridas} CORRIDAS")

    plt.show()


def graficar_esperanza(esperanza_matematica_listado, es_promedio):
    fig, ax = plt.subplots()

    ax.set_ylabel('vp (valor promedio de las tiradas)')
    ax.set_xlabel('n (numero tiradas)')

    for esperanza_matematica in esperanza_matematica_listado:
        ax.plot([i for i in range(cantidad_tiradas)], esperanza_matematica, linewidth=2.0, )

    ax.axhline(y=esperanza_matematica_esperada, color='r', linestyle='--', label='vpe (valor promedio esperado)')

    ax.legend()

    if es_promedio:
        ax.set_title(f"ESPERANZA MATEMATICA PROMEDIO {cantidad_corridas} CORRIDAS")
    else:
        ax.set_title(f"ESPERANZA MATEMATICA {cantidad_corridas} CORRIDAS")

    plt.show()


def graficar_histograma(frecuencias_listado, es_promedio):
    fig, ax = plt.subplots()

    ax.set_xlabel('n')
    ax.set_ylabel('fr (frecuencia relativa)')

    for df_frecuencias in frecuencias_listado:
        ax.bar(df_frecuencias['valor'], df_frecuencias['fr%'], alpha=0.5)

    ax.axhline((1 / 37) * 100, color='r', linestyle='--', label='fre (frecuencia relativa esperada)')

    ax.legend()

    if es_promedio:
        ax.set_title(f"HISTOGRAMA PROMEDIO {cantidad_corridas} CORRIDAS")
    else:
        ax.set_title(f"HISTOGRAMA {cantidad_corridas} CORRIDAS")

    plt.show()


def generar_dataframe_frecuencias(df_tiradas):
    frecuencia_absoluta = pd.Series(df_tiradas["valor"]).value_counts()

    df_frecuencias = pd.DataFrame()
    df_frecuencias['valor'] = frecuencia_absoluta.index
    df_frecuencias['fa'] = frecuencia_absoluta.values
    df_frecuencias['fr'] = df_frecuencias['fa'] / len(df_tiradas)
    df_frecuencias['fr%'] = 100 * df_frecuencias['fr']

    df_ordenado = df_frecuencias.sort_values(by='valor')

    return df_ordenado


def generar_estadisticas(numero_elegido):
    frecuencia_absoluta = []
    frecuencia_relativa = []
    esperanza_matematica = []
    desviacion_estandar = []
    varianza = []

    cantidad_ocurrencias = 0

    for index, tirada in enumerate(tiradas):
        if tirada == numero_elegido:
            cantidad_ocurrencias += 1
            frecuencia_absoluta.append(cantidad_ocurrencias)

        frecuencia_relativa.append(cantidad_ocurrencias / (index + 1))
        esperanza_matematica.append(np.mean(tiradas[:index + 1]))
        desviacion_estandar.append(np.std(tiradas[:index + 1]))
        varianza.append(np.var(tiradas[:index + 1]))

    return frecuencia_relativa, esperanza_matematica, desviacion_estandar, varianza


frecuencia_histograma_total = []
frecuencia_relativa_total = []
esperanza_matematica_total = []
desviacion_estandar_total = []
varianza_total = []

frecuencia_histograma_promedio = []
frecuencia_relativa_promedio = []
esperanza_matematica_promedio = []
desviacion_estandar_promedio = []
varianza_promedio = []

df_histograma_promedio = pd.DataFrame()

for corrida in range(cantidad_corridas):

    tiradas = np.random.randint(0, 37, size=[cantidad_tiradas])
    df_tiradas = pd.DataFrame(data=tiradas, columns=["valor"])

    df_frecuencias = generar_dataframe_frecuencias(df_tiradas)

    frecuencia_relativa, esperanza_matematica, desviacion_estandar, varianza = generar_estadisticas(numero_elegido)

    frecuencia_histograma_total.append(df_frecuencias)
    frecuencia_relativa_total.append(frecuencia_relativa)
    esperanza_matematica_total.append(esperanza_matematica)
    desviacion_estandar_total.append(desviacion_estandar)
    varianza_total.append(varianza)

    if not df_histograma_promedio.empty:
        df_histograma_promedio['fa'] += df_frecuencias['fa']
    else:
        df_histograma_promedio = df_frecuencias

df_histograma_promedio["fr"] = df_histograma_promedio["fa"] / (cantidad_tiradas * cantidad_corridas)
df_histograma_promedio["fr%"] = 100 * df_histograma_promedio["fr"]

frecuencia_histograma_promedio.append(df_histograma_promedio)
frecuencia_relativa_promedio.append(
    [sum(sublista[i] for sublista in frecuencia_relativa_total) / cantidad_corridas for i in range(cantidad_tiradas)])
esperanza_matematica_promedio.append(
    [sum(sublista[i] for sublista in esperanza_matematica_total) / cantidad_corridas for i in range(cantidad_tiradas)])
desviacion_estandar_promedio.append(
    [sum(sublista[i] for sublista in desviacion_estandar_total) / cantidad_corridas for i in range(cantidad_tiradas)])
varianza_promedio.append(
    [sum(sublista[i] for sublista in varianza_total) / cantidad_corridas for i in range(cantidad_tiradas)])

graficar_histograma(frecuencia_histograma_total, False)
graficar_frecuencia(frecuencia_relativa_total, False)
graficar_esperanza(esperanza_matematica_total, False)
graficar_desvio(desviacion_estandar_total, False)
graficar_varianza(varianza_total, False)
graficar_histograma(frecuencia_histograma_promedio, True)
graficar_frecuencia(frecuencia_relativa_promedio, True)
graficar_esperanza(esperanza_matematica_promedio, True)
graficar_desvio(desviacion_estandar_promedio, True)
graficar_varianza(varianza_promedio, True)
