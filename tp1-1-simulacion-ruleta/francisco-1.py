import matplotlib.pyplot as plt
import random

tiradas = 1000
numero_esperado = 14
# numero = 8

frecuencias_absolutas = [0 for _ in range(tiradas)]
frecuencias_relativas = [0 for _ in range(tiradas)]


fig, ax = plt.subplots()
cantidad = 0

for num_tiradas in range(1,tiradas):
    numero_obtenido = random.randint(1,36)
    if numero_obtenido == numero_esperado:
        cantidad+=1
    frecuencias_absolutas[num_tiradas] = cantidad
    frecuencias_relativas[num_tiradas] = frecuencias_absolutas[num_tiradas]/num_tiradas



# plot

ax.plot([i for i in range(tiradas)], frecuencias_relativas, linewidth=2.0, )
# agrego linea horizontal en y = 1/36 con nombre "Equilibrio"
ax.set_title('Gráfico 1: Valores Aleatorios')
ax.set_ylabel('fr (frecuencia relativa)')
ax.set_xlabel('n (numero tiradas)')
ax.axhline(y=1/36, color='r', linestyle='--', label='Equilibrio')
plt.show()
print(frecuencias_absolutas)
print(frecuencias_relativas)