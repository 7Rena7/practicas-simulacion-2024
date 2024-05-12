import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from estrategia import Estrategia


class Dalambert(Estrategia):
    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f'):
        super().__init__(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)

        self.es_capital_infinito = True if tipo_capital == 'i' else False
        self.capital = self.capital_inicial

    def estrategia(self, is_win):
        """
        Implementa un sistema de apuestas basado en la estrategia de D'alambert.

        Si la apuesta es ganadora, entonces se dismunye la cantidad apostada en una unidad
        SI la apuesta es perdedora, se aumenta la cantidad apostada en una unidad

        Parameters:
        listado_apuestas (list): Lista que contiene los montos de las apuestas previas.
        is_win (bool): Indica si la última apuesta fue ganadora (True) o perdedora (False).

        Returns:
        int: El monto de la próxima apuesta según la estrategia Fibonacci.
        """

        ultima_apuesta = self.listado_apuestas[-1]
        unidad = self.apuesta_inicial
        if is_win:
            self.capital += ultima_apuesta
            # Evitar apuestas menores que la unidad inicial
            proxima_apuesta = max(ultima_apuesta - unidad, unidad)
        else:
            self.capital -= ultima_apuesta
            proxima_apuesta = ultima_apuesta + unidad

        return proxima_apuesta

    def inicializar_valores(self):
        self.listado_apuestas = []
        self.listado_capital = []
        self.listado_unidades = []
        self.listado_wins = []
        self.listado_apuestas.append(self.apuesta_inicial)
        self.listado_capital.append(self.capital)
        self.listado_unidades.append(1)
        self.capital = self.capital_inicial

    def grafico_flujo_caja(self, listados_capital):
        plt.subplots(figsize=(10, 5))

        color = 'tab:blue'
        plt.xlabel('Número de Tiradas')
        plt.ylabel('Capital Total')

        for _, listado_capital in enumerate(listados_capital):
            plt.plot(listado_capital, alpha=0.75)

        plt.axhline(y=self.capital_inicial, color='r',
                    linestyle='-', label='Capital total')
        plt.tick_params(axis='y', labelcolor=color)
        plt.grid(True)

        plt.legend()
        plt.show()

    def generar_graficos(self, data_simulacion):
        # listados_capital = [df['capital'].tolist() for df in data_simulacion]
        listados_capital = [df['capital'] for df in data_simulacion]
        self.grafico_flujo_caja(listados_capital)

    def ejecutar_estrategia(self):
        data_simulacion = []
        for _ in range(0, self.cant_corridas):
            data_simulacion.append(self.simulacion())

        self.generar_graficos(data_simulacion)

    def simulacion(self):

        self.inicializar_valores()

        tirada = 0
        while True:
            tirada += 1
            numero_al_girar_ruleta = np.random.randint(0, 37)
            is_win = numero_al_girar_ruleta in self.resultados_rojo

            self.listado_wins.append(is_win)
            proxima_apuesta = self.estrategia(is_win)

            if not self.es_capital_infinito and proxima_apuesta > self.capital:  # banca rota
                break

            if self.es_capital_infinito and len(self.listado_apuestas) == self.cant_tiradas:
                break

            self.listado_unidades.append(
                self.listado_unidades[-1] + 1 if is_win else self.listado_unidades[-1] - 1)
            # listado_unidades.append( sum(listado_unidades) +1 if is_win else sum(listado_unidades) -1 )
            self.listado_apuestas.append(proxima_apuesta)
            self.listado_capital.append(self.capital)

        return pd.DataFrame({
            'apuesta': self.listado_apuestas,
            'win': self.listado_wins,
            'capital': self.listado_capital,
            'balance': self.listado_unidades})


if __name__ == "__main__":
    # Definimos los parámetros
    cant_tiradas = 1000  # Cantidad máxima de tiradas por corrida
    cant_corridas = 5  # Cantidad de corridas a simular
    numero_elegido = 'rojo'  # Podría ser también 'negro'
    tipo_capital = 'f'  # 'i' para capital infinito, 'f' para capital fijo

    # Creamos la instancia
    estrategia = Dalambert(cant_tiradas, cant_corridas,
                           numero_elegido, tipo_capital)

    # Ejecutamos la estrategia
    estrategia.ejecutar_estrategia()
