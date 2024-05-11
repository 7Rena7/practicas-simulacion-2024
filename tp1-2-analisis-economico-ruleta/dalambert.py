import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from estrategia import Estrategia

 
CAPITAL = 10000
APUESTA_INICIAL = 100

class Dalambert(Estrategia):
    def __init__(self, cant_tiradas, cant_corridas, numero_elegido, tipo_capital='i' or 'f'):
        super().__init__(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)

        # self.listado_apuestas = []
        # self.listado_capital = []
        # self.listado_unidades = []
        # self.listado_wins = []
        self.es_capital_infinito = True if tipo_capital == 'i' else False
        
        self.capital = 0
        
        self.apuesta_inicial = APUESTA_INICIAL
        self.rojo = [1, 3, 5, 7, 9, 12, 14, 16,
                     18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    
    def estrategia(self,is_win):
    # def estrategia(self,listado_apuestas,is_win):
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

        # global capital, apuesta_inicial
        ultima_apuesta = self.listado_apuestas[-1]
        unidad = self.apuesta_inicial 
        if is_win:
            self.capital += ultima_apuesta
            proxima_apuesta = max(ultima_apuesta - unidad, unidad)  # Evitar apuestas menores que la unidad inicial
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
        self.capital = CAPITAL

    def grafico_flujo_caja(self,listados_capital):
        fig, ax1 = plt.subplots(figsize=(20, 10))

        # Configuración del primer eje Y para el capital
        color = 'tab:blue'
        ax1.set_xlabel('Número de Tiradas')
        # ax1.set_ylabel('Capital Total', color=color)
        ax1.set_ylabel('Capital Total')

        for corrida, listado_capital in enumerate(listados_capital):
            print(corrida,listado_capital)
            ax1.plot(listado_capital, label=f'Corrida {corrida+1}', alpha=0.5)

        ax1.axhline(y=CAPITAL, color='r', linestyle='-', label='Capital total')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True)

        # Configuración de ticks del eje X cada 10 tiradas
        # max_len = max(len(listado) for listado in listados_capital)
        # ticks = np.arange(0, max_len, int(max_len/10))
        # ax1.set_xticks(ticks)
        # ax1.set_xticklabels(ticks)

        ax1.legend()
        plt.show()



    def generar_graficos(self, data_simulacion):
        # listados_capital = [df['capital'].tolist() for df in data_simulacion]
        listados_capital = [df['capital'] for df in data_simulacion]
        self.grafico_flujo_caja(listados_capital)


    def ejecutar_estrategia(self):
        data_simulacion = []
        for i in range(0,self.cant_corridas):
            print("Iteracion",i)
            data_simulacion.append(self.simulacion())

        self.generar_graficos(data_simulacion)

    
    def simulacion(self):

        self.inicializar_valores()

        tirada = 0
        while True:  
            tirada += 1
            numero_al_girar_ruleta = np.random.randint(0,37)
            is_win = numero_al_girar_ruleta in self.rojo

            self.listado_wins.append(is_win)
            proxima_apuesta = self.estrategia(is_win)
            
            if not self.es_capital_infinito and proxima_apuesta > self.capital: # banca rota
                break

            if self.es_capital_infinito and len(self.listado_apuestas) == self.cant_tiradas:
                break

            self.listado_unidades.append(self.listado_unidades[-1] +1 if is_win else self.listado_unidades[-1] -1 )
            # listado_unidades.append( sum(listado_unidades) +1 if is_win else sum(listado_unidades) -1 )
            self.listado_apuestas.append(proxima_apuesta)
            self.listado_capital.append(self.capital)

        return pd.DataFrame({
                'apuesta': self.listado_apuestas,
                'win': self.listado_wins,
                'capital': self.listado_capital,
                'balance': self.listado_unidades
                        })

if __name__ == "__main__":
    # Definimos los parámetros
    cant_tiradas = 1000  # Cantidad máxima de tiradas por corrida
    cant_corridas = 5  # Cantidad de corridas a simular
    numero_elegido = 'rojo'  # Podría ser también 'negro'
    tipo_capital = 'f'  # 'i' para capital infinito, 'f' para capital fijo

    # Creamos la instancia
    estrategia = Dalambert(cant_tiradas, cant_corridas, numero_elegido, tipo_capital)

    # Ejecutamos la estrategia
    estrategia.ejecutar_estrategia()



        # def grafico_flujo_caja(listado_capital):    
        
    #     fig, ax1 = plt.subplots(figsize=(20, 10))

    #     # Configuración del primer eje Y para el capital
    #     color = 'tab:blue'
    #     ax1.set_xlabel('Número de Tiradas')
    #     ax1.set_ylabel('Capital Total', color=color)
    #     ax1.plot(listado_capital, label='Capital Total', color=color)
    #     ax1.axhline(y=CAPITAL, color='r', linestyle='-', label='Capital total')

    #     # Ganancia maxima
    #     max_value =max(listado_capital)
    #     max_index = listado_capital.index(max_value)
    #     ax1.axvline(x=max_index, color='b', linestyle='--', label='Ganancia máxima')
    #     ax1.axhline(y=max_value, color='b', linestyle='--')
    #     ax1.scatter([max_index], [max_value], color='b', s=100)
    #     ax1.annotate(f'({max_value:.2f}, {max_index})', 
    #                 (max_index, max_value), 
    #                 textcoords="offset points", 
    #                 xytext=(50,10), 
    #                 color="b",
    #                 ha='center')

    #     # ax1.ax()
    #     ax1.tick_params(axis='y', labelcolor=color)
    #     ax1.grid(True)

    #     # Configuración de ticks del eje X cada 10 tiradas
    #     ticks = np.arange(0, len(listado_capital),int(len(listado_capital)/10))
    #     ax1.set_xticks(ticks)
    #     ax1.set_xticklabels(ticks)