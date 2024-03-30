import matplotlib.pyplot as plt
import random
from math import sqrt

tiradas = 500
numero_esperado = 36
ruleta_cantidad = 36
# numero = 8

frecuencias_absolutas = [0 for _ in range(tiradas)]
frecuencias_relativas = [0 for _ in range(tiradas)]
valores_tiradas = [0 for _ in range(tiradas)]
valores_promedio = [0 for _ in range(tiradas)]
desviaciones_tipicas = [0 for _ in range(tiradas)]

varianza = lambda xi,u,n : (xi-u)**2/n
desviacion = lambda xi,u,n : sqrt(varianza(xi,u,n))

fig, ax = plt.subplots()
cantidad = 0

for num_tiradas in range(1,tiradas):
    numero_obtenido = random.randint(1,ruleta_cantidad)
    if numero_obtenido == numero_esperado:
        cantidad+=1

    valores_tiradas[num_tiradas] =  numero_obtenido
    valores_promedio[num_tiradas] = sum(valores_tiradas)/num_tiradas
    desviaciones_tipicas[num_tiradas] = desviacion(numero_obtenido, valores_promedio[num_tiradas], num_tiradas)
    # frecuencias_absolutas[num_tiradas] = cantidad
    frecuencias_relativas[num_tiradas] = cantidad/num_tiradas
    


# plot

ax.plot([i for i in range(tiradas)], frecuencias_relativas, linewidth=2.0, )
ax.set_title('Gráfico 1')
ax.set_ylabel('fr (frecuencia relativa)')
ax.set_xlabel('n (numero tiradas)')
ax.axhline(y=1/36, color='r', linestyle='--', label='Equilibrio')
plt.show()

# print(frecuencias_absolutas)
# print(frecuencias_relativas)

fig, ax2 = plt.subplots()
ax2.plot([i for i in range(tiradas)], valores_tiradas, linewidth=2.0, )
ax2.set_title('Gráfico 2')
ax2.set_ylabel('μ (Valor promedio de tiradas)')
ax2.set_xlabel('n (numero tiradas)')
ax2.axhline(y=sum(valores_tiradas)/tiradas, color='r', linestyle='--', label='Media aritmetica')
plt.show()


fig, ax3 = plt.subplots()
ax3.plot([i for i in range(tiradas)], desviaciones_tipicas, linewidth=2.0, )
ax3.set_title('Gráfico 3')
ax3.set_ylabel('σ (Desviacion tipica)')
ax3.set_xlabel('n (numero tiradas)')
ax3.axhline(y=0, color='r', linestyle='--', label='Media aritmetica')
plt.show()


