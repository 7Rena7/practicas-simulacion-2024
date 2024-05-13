import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from estrategia import Estrategia

class Fibonacci(Estrategia):
    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f',):
        super().__init__(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)
        self.tiradas = np.random.randint(0, 37, size=[self.cant_tiradas])
        self.listado_apuestas_total = []
        self.listado_capital_total = []
        self.listado_wins_total = []
        self.listado_frecuencia_total = []
        self.listado_dfs = []
        self.capital_inicial = self.capital_inicial if tipo_capital == "f" else 0

    def ejecutar_estrategia(self):
        print('Ejecutando estrategia de Fibonacci...')
        
        for corrida in range(self.cant_corridas):

            capital = self.capital_inicial
            tiradas = np.random.randint(0,37,size=[self.cant_tiradas])

            listado_apuestas = []
            listado_capital = []
            listado_wins = []
            listado_frecuencia_relativa = []

            listado_apuestas.append(self.apuesta_inicial)
            listado_capital.append(capital)

            for index, tirada in enumerate(tiradas):
                
                is_win = tirada in self.resultados_rojo
                listado_wins.append(is_win)

                listado_frecuencia_relativa.append(listado_wins.count(True)/(index+1))

                proxima_apuesta, capital = self.fibonacci(listado_apuestas, is_win, capital)
                print(proxima_apuesta)
                print(f"capital {capital}")
                
                if proxima_apuesta > capital and self.tipo_capital == 'f': # banca rota
                    break

                if len(listado_apuestas) == self.cant_tiradas:
                    break
                
                listado_apuestas.append(proxima_apuesta)
                listado_capital.append(capital)
                
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
        
    def fibonacci(self, listado_apuestas, is_win, capital):
            """
            Implementa un sistema de apuestas basado en la estrategia de progresión Fibonacci.
            Si la apuesta es ganadora, se retrocede dos posiciones en el listado.
            Si la apuesta es perdedora, se suma el valor de las ultmas dos apuestas.

            Parameters:
            listado_apuestas (list): Lista que contiene los montos de las apuestas previas.
            is_win (bool): Indica si la última apuesta fue ganadora (True) o perdedora (False).

            Returns:
            int: El monto de la próxima apuesta según la estrategia Fibonacci.
            """
            ultima_apuesta = listado_apuestas[-1]
            if is_win:
                capital += ultima_apuesta
                proxima_apuesta = max(listado_apuestas[-3] if len(listado_apuestas) > 2 else ultima_apuesta, self.apuesta_inicial)
            else:
                capital -= ultima_apuesta
                proxima_apuesta = max(sum(listado_apuestas[-2:]) if len(listado_apuestas) > 1 else ultima_apuesta, self.apuesta_inicial)

            return proxima_apuesta, capital
    
    def grafico_flujo_caja(self):        
        fig, ax = plt.subplots()

        ax.set_title(f"ESTRATEGIA FIBONACCI CAPITAL {self.tipo_capital}")
        ax.set_xlabel('n (número de tiradas)')
        ax.set_ylabel('cc (cantidad de capital)')

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