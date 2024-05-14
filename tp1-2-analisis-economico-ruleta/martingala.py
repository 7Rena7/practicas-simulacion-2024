import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from estrategia import Estrategia


class Martingala(Estrategia):

    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f'):
        super().__init__(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)
        self.tiradas = np.random.randint(0, 37, size=[self.cant_tiradas])
        self.listado_apuestas = []
        self.listado_capital = []
        self.listado_wins = []
        self.capital = self.capital_inicial

    def ejecutar_estrategia(self):
        self.listado_apuestas.append(self.apuesta_inicial)
        self.listado_capital.append(self.capital)

        for tirada in self.tiradas:
            is_win = tirada in self.resultados_rojo
            self.listado_wins.append(is_win)

            proxima_apuesta = self.martingala(
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

    def martingala(self, apuesta_actual, is_win):
        """
        Implementa la estrategia de apuestas de Martingala.
        Si la apuesta es ganadora, se vuelve a apostar la apuesta inicial.
        Si la apuesta es perdedora, se duplica la apuesta.

        Parameters:
        apuesta_actual (float): La cantidad apostada en la última tirada.
        is_win (bool): Indica si la última apuesta fue ganadora (True) o perdedora (False).

        Returns:
        float: El monto de la próxima apuesta según la estrategia de Martingala.
        """
        if is_win:
            self.capital += apuesta_actual
            proxima_apuesta = self.apuesta_inicial
        else:
            self.capital -= apuesta_actual
            proxima_apuesta = apuesta_actual * 2

        return proxima_apuesta

    def grafico_flujo_caja(self):
        global cantidad_tiradas

        _, ax = plt.subplots()

        ax.set_title(
            f"ESTRATEGIA MARTINGALA - CAPITAL INICIAL: {self.listado_capital[0]}")
        ax.set_xlabel('n (Número de tiradas)')
        ax.set_ylabel('cc (Cantidad de capital)')

        ax.plot([i for i in range(1, len(self.listado_apuestas) + 1)],
                self.listado_capital, linewidth=2.0, label='fc (Flujo de caja)')
        ax.axhline(self.listado_capital[0], color='r',
                   linestyle='--', label='fci (Flujo de caja inicial)')

        plt.legend()
        plt.show()

# Como estaba antes de la refactorización a clase Martingala 👇🏽👇🏽👇🏽
# if __name__ == "__main__":
#     cantidad_tiradas = 10000
#     apuesta_inicial = 1
#     capital = 100
#     tipo_capital = 'f'
#     rojo = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

#     def martingala(apuesta_actual, is_win):
#         """
#         Implementa la estrategia de apuestas de Martingala.
#         Si la apuesta es ganadora, se vuelve a apostar la apuesta inicial.
#         Si la apuesta es perdedora, se duplica la apuesta.

#         Parameters:
#         apuesta_actual (float): La cantidad apostada en la última tirada.
#         is_win (bool): Indica si la última apuesta fue ganadora (True) o perdedora (False).

#         Returns:
#         float: El monto de la próxima apuesta según la estrategia de Martingala.
#         """
#         global capital, apuesta_inicial

#         if is_win:
#             capital += apuesta_actual
#             proxima_apuesta = apuesta_inicial
#         else:
#             capital -= apuesta_actual
#             proxima_apuesta = apuesta_actual * 2

#         return proxima_apuesta

#     tiradas = np.random.randint(0, 37, size=[cantidad_tiradas])
#     listado_apuestas = []
#     listado_capital = []
#     listado_wins = []

#     listado_apuestas.append(apuesta_inicial)
#     listado_capital.append(capital)

#     for tirada in tiradas:
#         is_win = tirada in rojo
#         listado_wins.append(is_win)

#         proxima_apuesta = martingala(listado_apuestas[-1], is_win)

#         if proxima_apuesta > capital and tipo_capital == 'f':  # banca rota
#             break

#         if len(listado_apuestas) == cantidad_tiradas:
#             break

#         listado_apuestas.append(proxima_apuesta)
#         listado_capital.append(capital)

#     # Crear DataFrame
#     df = pd.DataFrame({
#         'apuesta': listado_apuestas,
#         'win': listado_wins,
#         'capital': listado_capital
#     })

#     # Función para graficar el flujo de caja

#     def grafico_flujo_caja(listado_capital):
#         global cantidad_tiradas

#         fig, ax = plt.subplots()

#         ax.set_title(
#             f"ESTRATEGIA MARTINGALA - CAPITAL INICIAL: {listado_capital[0]}")
#         ax.set_xlabel('n (Número de tiradas)')
#         ax.set_ylabel('cc (Cantidad de capital)')

#         ax.plot([i for i in range(1, len(listado_apuestas) + 1)],
#                 listado_capital, linewidth=2.0, label='fc (Flujo de caja)')
#         ax.axhline(listado_capital[0], color='r',
#                    linestyle='--', label='fci (Flujo de caja inicial)')

#         plt.legend()
#         plt.show()

#     # Mostrar gráfico
#     grafico_flujo_caja(listado_capital)
