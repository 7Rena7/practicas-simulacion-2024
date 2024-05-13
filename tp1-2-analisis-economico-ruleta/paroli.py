import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from estrategia import Estrategia


class Paroli(Estrategia):
    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f', ):
        super().__init__(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)
        self.tiradas = np.random.randint(0, 37, size=[self.cant_tiradas])
        self.listado_apuestas = []
        self.listado_capital = []
        self.listado_wins = []
        self.capital = self.capital_inicial
        self.victorias_seguidas = 0

    def paroli(self, ultima_apuesta, is_win):
        """
        Implementa un sistema de apuestas basado en el sistema de Paroli.

        Primero se apuesta la mínima.
        Si la apuesta es ganadora, entonces se duplica la cantidad apostada, hasta llegar a 3 victorias consecutivas.
        Al llegar a 3 victorias consecutivas, se reinicia la apuesta y se vuelve a apostar la mínima.
        Si la apuesta es perdedora, se apuesta lo mínimo.

        Parameters:
        apuesta_actual (float): La cantidad apostada en la última tirada.
        is_win (bool): Indica si la última apuesta fue ganadora (True) o perdedora (False).

        Returns:
        int: El monto de la próxima apuesta según la estrategia de Paroli.
        """
        if is_win:
            self.victorias_seguidas += 1
            self.capital += ultima_apuesta

            if self.victorias_seguidas == 3:
                self.victorias_seguidas = 0
                proxima_apuesta = self.apuesta_inicial
            else:
                proxima_apuesta = ultima_apuesta * 2
        else:
            self.victorias_seguidas = 0
            self.capital -= ultima_apuesta
            proxima_apuesta = self.apuesta_inicial

        return proxima_apuesta

    def grafico_flujo_caja(self):
        global cantidad_tiradas

        _, ax = plt.subplots()

        ax.set_title(
            f"ESTRATEGIA PAROLI - CAPITAL INICIAL: {self.listado_capital[0]}")
        ax.set_xlabel('n (Número de tiradas)')
        ax.set_ylabel('cc (Cantidad de capital)')

        ax.plot([i for i in range(1, len(self.listado_apuestas) + 1)],
                self.listado_capital, linewidth=2.0, label='fc (Flujo de caja)')
        ax.axhline(self.listado_capital[0], color='r',
                   linestyle='--', label='fci (Flujo de caja inicial)')

        plt.legend()
        plt.show()

    def ejecutar_estrategia(self):
        self.listado_apuestas.append(self.apuesta_inicial)
        self.listado_capital.append(self.capital)

        for tirada in self.tiradas:
            """
            El sistema de Paroli no indica qué se debe apostar, si no cuanto según la cantidad de victorias seguidas.
            Por lo tanto, como ejemplo para hacer una prueba, apuesto siempre al rojo.
            """
            is_win = tirada in self.resultados_rojo
            self.listado_wins.append(is_win)

            proxima_apuesta = self.paroli(
                self.listado_apuestas[-1], is_win)

            if proxima_apuesta > self.capital and self.tipo_capital == 'f':  # banca rota
                break

            if len(self.listado_apuestas) == self.cant_tiradas:
                break

            self.listado_apuestas.append(proxima_apuesta)
            self.listado_capital.append(self.capital)

        # Crear DataFrame
        df = pd.DataFrame({
            'apuesta': self.listado_apuestas,
            'win': self.listado_wins,
            'capital': self.listado_capital
        })

        # Mostrar gráfico
        self.grafico_flujo_caja()
