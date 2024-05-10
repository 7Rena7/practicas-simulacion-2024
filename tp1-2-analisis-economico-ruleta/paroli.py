from estrategia import Estrategia

class Paroli(Estrategia):
    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f',):
        super().__init__(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)

    def ejecutar_estrategia(self):
        print('Ejecutando estrategia de Paroli...')