import matplotlib.pyplot as plt
from random import randint 
from sys import argv as arguments, exit
from os import path as filepath

# Verificar si se proporciona el número correcto de argumentos en la línea de comandos. Se deben proporcionar seis
# argumentos: -c <num_tiradas> -n <num_corridas> -e <numero_elegido>. Todos los argumentos deben ser enteros, -c debe
# estar entre 1 y 1000, -n debe estar entre 1 y 100, y -e debe estar entre 0 y 36
if len(arguments) != 7 or arguments[1] != "-c" or arguments[3] != "-n" or arguments[5] != "-e":
    print("La cantidad de argumentos o su orden es incorrecta.\n")
    print("Uso: python/python3 {} -c <cantidad_de_tiradas>[int 1-1000] -n <cantidad_de_corridas>[int 1-100] -e "
          "<numero_elegido>[int 0-36]\n".format(filepath.basename(__file__)))
    print("Ejemplo: python/python3 {} -c 1000 -n 10 -e 8".format(filepath.basename(__file__)))
    exit(1)

# Obtener el número de tiradas, corridas y el número seleccionado de los argumentos de la línea de comandos
tiradas = int(arguments[2])
corridas = int(arguments[4])
numero_esperado = int(arguments[6])
cantidad_ruleta = 36

if not (1 <= tiradas <= 1000):
    print("El número de tiradas debe estar entre 1 y 1000.")
    exit(1)

if not (1 <= corridas <= 100):
    print("El número de corridas debe estar entre 1 y 1000.")
    exit(1)

if not (0 <= numero_esperado <= 36):
    print("El número elegido debe estar entre 0 y 36.")
    exit(1)

print("***** Simulación de una Ruleta ***** \n"
      "Número de Tiradas: {} \n"
      "Número de Corridas: {} \n"
      "Número Elegido: {} \n"
      .format(tiradas, corridas, numero_esperado))

  
cantidad = 0
valores_tiradas = []
valores_promedio = []
desviaciones_tipicas = []
varianzas = []
frecuencias_relativas = []

frecuencia_relativa = lambda x,n: x/n
media = lambda valores : sum(valores)/len(valores)
varianza = lambda valores,media: sum((xi - media)**2 for xi in valores) / len(valores)
desviacion_estandar = lambda varianza: varianza ** 0.5

for num_tiradas in range(1, tiradas + 1):
    numero_obtenido = randint(1, cantidad_ruleta)
    if numero_obtenido == numero_esperado:
        cantidad += 1
 
    valores_tiradas.append(numero_obtenido)

    promedio_actual = media(valores_tiradas)
    frecuencia_relativa_actual = frecuencia_relativa(cantidad,num_tiradas)
    varianza_actual = varianza(valores_tiradas,promedio_actual)
    desviacion_actual = desviacion_estandar(varianza_actual) 

    valores_promedio.append(promedio_actual)
    varianzas.append(varianza_actual)
    desviaciones_tipicas.append(desviacion_actual)
    frecuencias_relativas.append(frecuencia_relativa_actual)

 
fig, axs = plt.subplots(1, 4, figsize=(18, 6))

axs[0].plot(frecuencias_relativas, linewidth=2.0)
axs[0].set_title('Frecuencia Relativa vs Numero de Tiradas')
axs[0].axhline(y=1/cantidad_ruleta, color='r', linestyle='--')

axs[1].plot(valores_promedio, linewidth=2.0)
axs[1].set_title('Valor Promedio de Tiradas vs Numero de Tiradas')
axs[1].axhline(y=media(valores_tiradas), color='r', linestyle='--')

axs[2].plot(desviaciones_tipicas, linewidth=2.0)
axs[2].set_title('Desviacion Tipica vs Numero de Tiradas')

axs[3].plot(varianzas, linewidth=2.0)
axs[3].set_title('Valor de la varianza vs Numero de Tiradas')
 
plt.tight_layout()
plt.savefig('resultados.png')
plt.show()