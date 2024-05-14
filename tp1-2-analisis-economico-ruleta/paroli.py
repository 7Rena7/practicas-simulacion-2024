import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from estrategia import Estrategia


class Paroli(Estrategia):
    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f', ):
        super().__init__(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)
        self.listado_apuestas_total = []
        self.listado_capital_total = []
        self.listado_wins_total = []
        self.listado_frecuencia_total = []
        self.listado_dfs = []
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
        ultima_apuesta (float): La cantidad apostada en la última tirada.
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
        fig, ax = plt.subplots()

        ax.set_title(f"ESTRATEGIA PAROLI CAPITAL {self.tipo_capital}")
        ax.set_xlabel('n (número de tiradas)')
        ax.set_ylabel('c (capital)')

        for listado_capital in self.listado_capital_total:
            ax.plot(listado_capital, linewidth=2.0, )

        ax.axhline(self.capital_inicial, color='r', linestyle='--', label='fci (flujo de caja inicial)')

        ax.ticklabel_format(axis='y', style='plain')

        plt.legend()
        plt.show()

    def graficar_histograma(self):
        fig, ax = plt.subplots()

        ax.set_title(f"HISTOGRAMA {self.cant_corridas} CORRIDAS")
        ax.set_xlabel('n (número de tiradas)')
        ax.set_ylabel('fr (frecuencia relativa)')

        for df in self.listado_dfs:
            ax.bar(df.index, df['fr'], alpha=0.5)

        plt.show()

    def ejecutar_estrategia(self):
        print('Ejecutando estrategia de Paroli...')

        for corrida in range(self.cant_corridas):

            self.capital = self.capital_inicial
            tiradas = np.random.randint(0, 37, size=[self.cant_tiradas])

            listado_apuestas = []
            listado_capital = []
            listado_wins = []
            listado_frecuencia_relativa = []

            listado_apuestas.append(self.apuesta_inicial)
            listado_capital.append(self.capital)

            for index, tirada in enumerate(tiradas):

                is_win = tirada in self.resultados_rojo
                listado_wins.append(is_win)

                listado_frecuencia_relativa.append(listado_wins.count(True) / (index + 1))

                proxima_apuesta = self.paroli(listado_apuestas[-1], is_win)

                if proxima_apuesta > self.capital and self.tipo_capital == 'f':  # banca rota
                    break

                if len(listado_apuestas) == self.cant_tiradas:
                    break

                listado_apuestas.append(proxima_apuesta)
                listado_capital.append(self.capital)

            self.listado_apuestas_total.append(listado_apuestas)
            self.listado_capital_total.append(listado_capital)
            self.listado_wins_total.append(listado_wins)
            self.listado_frecuencia_total.append(listado_frecuencia_relativa)

            df = pd.DataFrame({
                'capital': listado_capital,
                'apuesta': listado_apuestas,
                'win': listado_wins,
                'fr': listado_frecuencia_relativa
            })

            self.listado_dfs.append(df)

        # Mostrar gráfico
        self.grafico_flujo_caja()
        self.graficar_histograma()

