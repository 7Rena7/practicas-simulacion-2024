import matplotlib.pyplot as plt
import numpy as np
import random

from gcl_generator import generador_gcl
from mersenne_twister_generator import generador_mersenne_twister
from main import seed,m,c,a,n

# Transforma los números reales positivos a números enteros 0 o 1
def transf_a_binario(numeros):
    return [1 if x % 2 == 0 else 0 for x in numeros]

def crear_imagen_con_ruido(numbers, size):
    # Normaliza los números para que estén en el rango [0, 1]
    normalized_numbers = np.array(numbers) / max(numbers)
    # Devuelve una matriz cuadrada del tamaño de size
    noise_image = normalized_numbers.reshape(size, size)

    plt.imshow(noise_image, cmap='gray')
    plt.title('Ruido atmosferico - GCL')
    plt.axis('off')
    plt.savefig(f'./images/Ruido atmosferico GCL.png')
    plt.show()

def crear_imagen_con_ruido(numbers, size,nombre_generador):
    # Normaliza los números para que estén en el rango [0, 1]
    normalized_numbers = np.array(numbers) / max(numbers)
    # Devuelve una matriz cuadrada del tamaño de size
    noise_image = normalized_numbers.reshape(size, size)

    plt.imshow(noise_image, cmap='gray')
    plt.title(f'Ruido atmosferico - {nombre_generador}')
    plt.axis('off')
    plt.savefig(f'./images/Ruido atmosferico {nombre_generador}.png')
    plt.show()


def generar_ruido_por_paridad():
    numbers = generador_gcl(m, a, c, seed, n)
    numeros_mt = generador_mersenne_twister(seed, n)
    numeros_python = [random.randint(0, 2**32 - 1) for _ in range(n)]
 
    numeros_mt = transf_a_binario(numeros_mt)
    numeros_python = transf_a_binario(numeros_python)

    # crear_imagen_con_ruido(numbers,512)
    for numeros, nombre_generador in [
            (numbers, 'GCL'), 
            (numeros_mt, 'Mersenne Twister'), 
            (numeros_python, 'Python Random')]:
        
        crear_imagen_con_ruido(numbers,512,nombre_generador)
        # generar_imagen(numeros,nombre_generador)

def generar_imagen(numeros, nombre_generador,extra=''):
    # Inicializa un arreglo que representa una imagen en blanco (lleno de 0s)
    img = np.zeros((512, 512), dtype=np.uint8)

    for i in range(512):
        for j in range(512):
            # Colorear el píxel segun si el número aleatorio es 1
            if numeros[i * 512 + j] == 1:   #  índice lineal que convierte la coordenada 2D (i, j) en un índice 1D de la lista numeros.
                img[i, j] = 255  # valor de color blanco

    # Mostrar y guardar la imagen
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Ruido atmosferico {extra}- {nombre_generador}')
    plt.axis('off')
    plt.savefig(f'./images/Ruido atmosferico {extra}- {nombre_generador}.png')
    plt.show()

generar_ruido_por_paridad()