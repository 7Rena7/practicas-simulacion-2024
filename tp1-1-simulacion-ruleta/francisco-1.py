import matplotlib.pyplot as plt
from random import randint
from math import sqrt
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

ruleta_cantidad = 36
# numero = 8

frecuencias_absolutas = [0 for _ in range(tiradas)]
frecuencias_relativas = [0 for _ in range(tiradas)]
valores_tiradas = [0 for _ in range(tiradas)]
valores_promedio = [0 for _ in range(tiradas)]
desviaciones_tipicas = [0 for _ in range(tiradas)]

varianza = lambda xi,u,n : (xi-u)**2/n
desviacion = lambda xi,u,n : sqrt(varianza(xi,u,n))

cantidad = 0

for num_tiradas in range(1,tiradas):
    numero_obtenido = randint(1,ruleta_cantidad)
    if numero_obtenido == numero_esperado:
        cantidad+=1

    valores_tiradas[num_tiradas] =  numero_obtenido
    valores_promedio[num_tiradas] = sum(valores_tiradas)/num_tiradas
    desviaciones_tipicas[num_tiradas] = desviacion(numero_obtenido, valores_promedio[num_tiradas], num_tiradas)
    # frecuencias_absolutas[num_tiradas] = cantidad
    frecuencias_relativas[num_tiradas] = cantidad/num_tiradas

# Crear la figura y los subgráficos
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

axs[0].plot([i for i in range(tiradas)], frecuencias_relativas, linewidth=2.0, )
axs[0].set_title('Frecuencia Relativa vs Numero de Tiradas')
axs[0].set_ylabel('fr (frecuencia relativa)')
axs[0].set_xlabel('n (numero tiradas)')
axs[0].axhline(y=1/36, color='r', linestyle='--', label='Equilibrio')

axs[1].plot([i for i in range(tiradas)], valores_tiradas, linewidth=2.0, )
axs[1].set_title('Valor Promedio de Tiradas vs Numero de Tiradas')
axs[1].set_ylabel('μ (Valor promedio de tiradas)')
axs[1].set_xlabel('n (numero tiradas)')
axs[1].axhline(y=sum(valores_tiradas)/tiradas, color='r', linestyle='--', label='Media aritmetica')

axs[2].plot([i for i in range(tiradas)], desviaciones_tipicas, linewidth=2.0, )
axs[2].set_title('Desviacion Tipica vs Numero de Tiradas')
axs[2].set_ylabel('σ (Desviacion tipica)')
axs[2].set_xlabel('n (numero tiradas)')
axs[2].axhline(y=0, color='r', linestyle='--', label='Media aritmetica')

# Ajustar diseño y mostrar gráficos
plt.tight_layout()

# Guardar la figura en disco
plt.savefig('resultados.png')

# Mostrar la figura
plt.show()

