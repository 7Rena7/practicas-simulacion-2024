#OTRO ARCHIVO DISTINTO

import random
import matplotlib.pyplot as plt
import sys

num_elegido = 4

num_valores = 10

x1 = list(range(num_valores))
#y1 = [random.random() for _ in x1]
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

valores = [random.randint(0,36) for _ in range(num_valores)]
print("Valores generados:", valores)

#frecuencia_absoluta = {0: null, 1: null}
#for i in valores[i]
frecuencia_absoluta = [ 0 for _ in range(num_valores)]
frecuencias_relativas =  [0 for _ in range(num_valores)]

for i in valores:
    if num_elegido == i:
           frecuencia_absoluta[i] += 1
           frecuencias_relativas = frecuencia_absoluta[i]/num_valores

axs[0].plot(x1,frecuencias_relativas, color='blue')
axs[0].set_title('Gráfico 1: Valores Aleatorios')
axs[0].set_xlabel('Numero de tiradas')
axs[0].set_ylabel('Frecuencia relativa')

# Ajustar diseño y mostrar gráficos
plt.tight_layout()

# Guardar la figura en disco
plt.savefig('tres_graficas_valores_aleatorios.png')

# Mostrar la figura
plt.show()
