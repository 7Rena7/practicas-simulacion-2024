class Estrategia:
    capital_inicial = 10000
    apuesta_inicial = 1
    resultados_rojo = [1, 3, 5, 7, 9, 12, 14, 16,
                       18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f',):
        self.tipo_capital = tipo_capital
        self.cant_tiradas = cant_tiradas
        self.cant_corridas = cant_corridas
        self.numero_elegido = numero_elegido

    def ejecutar_estrategia(self):
        pass
