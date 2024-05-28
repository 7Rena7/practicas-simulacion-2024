import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import stats
from gcl_generator import generador_gcl
from mersenne_twister_generator import generador_mersenne_twister,generador_mersenne_twister_binario
from PIL import Image
from main import seed,m,c,a,n
# from main import seed,c,a

filas = 512
columnas = 512

n = filas * columnas

# Generar números pseudoaleatorios
# Asegurarse de que la longitud de los números generados sea correcta

def ajustar_longitud_lista(lista, tamano):
    if len(lista) < tamano:
        lista.extend([0] * (tamano - len(lista)))
    elif len(lista) > tamano:
        lista = lista[:tamano]
    return lista

# Transforma los números reales positivos a números enteros 0 o 1
def transf_lineal_a_binario(numeros):
    return [1 if x % 2 == 0 else 0 for x in numeros]

def generar_ruido_por_paridad():
    numeros_gcl = generador_gcl(m, a, c, seed, n)
    numeros_mt = generador_mersenne_twister(seed, n)
    numeros_python = [random.randint(0, 2**32 - 1) for _ in range(n)]
    
    numeros_gcl = ajustar_longitud_lista(numeros_gcl, n)
    numeros_mt = ajustar_longitud_lista(numeros_mt, n)
    numeros_python = ajustar_longitud_lista(numeros_python, n)

    numeros_gcl = transf_lineal_a_binario(numeros_gcl)
    numeros_mt = transf_lineal_a_binario(numeros_mt)
    numeros_python = transf_lineal_a_binario(numeros_python)


    for numeros, nombre_generador in [
            (numeros_gcl, 'GCL'), 
            (numeros_mt, 'Mersenne Twister'), 
            (numeros_python, 'Python Random')]:
        
        generar_imagen(numeros,nombre_generador)
 
def generar_ruido_por_binarios():
    numeros_gcl = generador_gcl(2, a, c, seed, n)
    numeros_mt = generador_mersenne_twister_binario(seed, n)
    numeros_python = [random.randint(0, 1) for _ in range(n)]

    numeros_gcl = ajustar_longitud_lista(numeros_gcl, n)
    numeros_mt = ajustar_longitud_lista(numeros_mt, n)
    numeros_python = ajustar_longitud_lista(numeros_python, n)

    for numeros, nombre_generador in [
            (numeros_gcl, 'GCL'), 
            (numeros_mt, 'Mersenne Twister'), 
            (numeros_python, 'Python Random')]:
        
        generar_imagen(numeros,nombre_generador)
    

# <?php
# // Requires the GD Library
# header("Content-type: image/png");
# $im = imagecreatetruecolor(512, 512)
#     or die("Cannot Initialize new GD image stream");
# $white = imagecolorallocate($im, 255, 255, 255);
# for ($y = 0; $y < 512; $y++) {
#     for ($x = 0; $x < 512; $x++) {
#         if (rand(0, 1)) {
#             imagesetpixel($im, $x, $y, $white);
#         }
#     }
# }		
# imagepng($im);
# imagedestroy($im);

def generar_imagen(numeros, nombre_generador):
    # Inicializa un arreglo que representa una imagen en blanco (lleno de 0s)
    img = np.zeros((512, 512), dtype=np.uint8)

    for i in range(512):
        for j in range(512):
            # Colorear el píxel segun si el número aleatorio es 1
            if numeros[i * 512 + j] == 1:   #  índice lineal que convierte la coordenada 2D (i, j) en un índice 1D de la lista numeros.
                img[i, j] = 255  # valor de color blanco

    # Mostrar y guardar la imagen
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Ruido atmosferico - {nombre_generador}')
    plt.axis('off')
    plt.savefig(f'Ruido atmosferico - {nombre_generador}.png')
    plt.show()


 
generar_ruido_por_binarios()