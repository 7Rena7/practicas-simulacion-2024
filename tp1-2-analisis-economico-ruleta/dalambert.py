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
        self.cantidad_ganadas = 0 
        self.listado_wins = []
        self.listado_frecuencia_relativa = []
        self.listado_apuestas.append(self.apuesta_inicial)
        self.capital = self.capital_inicial
        self.listado_capital.append(self.capital)
        self.listado_unidades.append(1)
 

    def generar_histograma(self,listado_dfs):
        fig, ax = plt.subplots()

        ax.set_title(f"HISTOGRAMA {self.cant_corridas} CORRIDAS")
        ax.set_xlabel('n (número de tiradas)')
        ax.set_ylabel('fr (frecuencia relativa)')

        for df in listado_dfs:
            ax.bar(df.index, df['fr'], alpha=1)

        plt.show()


    def generar_histograma_densidad(self, data_simulacion):
        """
        La idea es generar un histograma con la densidad de ganancia y pérdida, para intentar sacar su distribución
        y determinar si existe algún comportamiento sobre donde es conveniente salir del juego, ya sea ganando o perdiendo.
        """
        listados_capital = [df['capital'] for df in data_simulacion]

        ganancias_maximas = [] 
        perdidas_maximas = []
        for listado_capital in listados_capital:
            max_value = max(listado_capital)
            min_value = min(listado_capital)

            ganancias_maximas.append(((max_value * 100) / self.capital_inicial) - 100)
            perdidas_maximas.append(((min_value * 100) / self.capital_inicial) -100)

        fig, axs = plt.subplots(2, 1, figsize=(10, 8))

        axs[0].hist(ganancias_maximas, bins=10, alpha=1, color='green')
        axs[0].set_ylabel('Frecuencia')
        axs[0].set_xlabel('Proporción (%)')
        axs[0].set_title('Histograma de la proporción de ganancias máximas')

        axs[1].hist(perdidas_maximas, bins=10, alpha=1, color='red')
        axs[1].set_xlabel('Proporción (%)')
        axs[1].set_ylabel('Frecuencia')
        axs[1].set_title('Histograma de la proporción de pérdidas máximas')

        plt.tight_layout()
        plt.show()

                


    def grafico_flujo_caja(self,listados_capital):
        fig, ax1 = plt.subplots(figsize=(20, 10))

        # Configuración del primer eje Y para el capital
        color = 'tab:blue'
        ax1.set_xlabel('Número de Tiradas')
        # ax1.set_ylabel('Capital Total', color=color)
        ax1.set_ylabel('Capital Total')

        for corrida, listado_capital in enumerate(listados_capital):
            ax1.plot(listado_capital, label=f'Corrida {corrida+1}', alpha=1)
            max_value = max(listado_capital)
            ax1.scatter([0], [max_value])


        ax1.axhline(y=self.capital_inicial, color='r', linestyle='-', label='Capital total')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True)

        ax1.legend()
        plt.show()

    def grafico_flujo_caja_promedio(self, listados_capital):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Calcular el promedio del capital para cada tirada
        
        max_tiradas = max(len(listado) for listado in listados_capital)  # Obtener la longitud máxima de las listas
        promedio_capital = []
        for j in range(0,max_tiradas):
            sum_capital_en_tirada_i = 0    
            for i in range(0,len(listados_capital)):
                try:
                    sum_capital_en_tirada_i+=listados_capital[i][j]
                except:
                    sum_capital_en_tirada_i+=0
            promedio_capital.append(sum_capital_en_tirada_i/self.cant_corridas)
            

        # Graficar el promedio del capital
        ax.plot(promedio_capital, label='Promedio del Capital', color='blue')
        ax.set_title('Flujo de caja promedio a lo largo de las tiradas')
        ax.set_xlabel('Número de Tiradas')
        ax.set_ylabel('Capital Promedio')
        ax.legend()
        ax.grid(True)
        plt.show()


    def generar_histograma_promedio(self, listado_frecuencia_relativa):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        max_tiradas = max(len(listado) for listado in listado_frecuencia_relativa)  
        promedio_frecuencias = []

        for j in range(max_tiradas):
            sum_frecuencias_en_tirada_j = 0    
            for i in range(len(listado_frecuencia_relativa)):
                try:
                    sum_frecuencias_en_tirada_j += listado_frecuencia_relativa[i][j]
                except:
                    sum_frecuencias_en_tirada_j += 0
            promedio_frecuencias.append(sum_frecuencias_en_tirada_j / self.cant_corridas)

        # Use a proper range for the x values
        x_values = range(len(promedio_frecuencias))
        
        ax.set_title(f"HISTOGRAMA PROMEDIO DE {self.cant_corridas} CORRIDAS")
        ax.set_xlabel('n (número de tiradas)')
        ax.set_ylabel('fr (frecuencia relativa)')
        ax.bar(x_values, promedio_frecuencias, alpha=1)
        plt.show()




    def generar_graficos(self, data_simulacion):
        listados_capital = [df['capital'] for df in data_simulacion]
        listado_frecuencias_relativas = [df["fr"] for df in data_simulacion]

        self.grafico_flujo_caja(listados_capital)
        self.grafico_flujo_caja_promedio(listados_capital)
        self.generar_histograma(data_simulacion)
        self.generar_histograma_promedio(listado_frecuencias_relativas)


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

            if is_win:
                self.cantidad_ganadas += 1
            
            self.listado_wins.append(is_win)
            proxima_apuesta = self.estrategia(is_win)
            
            fr = self.cantidad_ganadas/(tirada)
            self.listado_frecuencia_relativa.append(fr)

            if not self.es_capital_infinito and proxima_apuesta > self.capital: # banca rota
                break

            if len(self.listado_apuestas) == self.cant_tiradas:
                break


            self.listado_unidades.append(self.listado_unidades[-1] +1 if is_win else self.listado_unidades[-1] -1 )
            self.listado_apuestas.append(proxima_apuesta)
            self.listado_capital.append(self.capital)

        return pd.DataFrame({
                'apuesta': self.listado_apuestas,
                'win': self.listado_wins,
                'capital': self.listado_capital,
                'balance': self.listado_unidades,
                'fr':self.listado_frecuencia_relativa
                        })

 
if __name__ == "__main__":
    # Definimos los parámetros
    cant_tiradas = 100  # Cantidad máxima de tiradas por corrida
    cant_corridas = 5  # Cantidad de corridas a simular
    numero_elegido = 'rojo'  # Podría ser también 'negro'
    tipo_capital = 'i'  # 'i' para capital infinito, 'f' para capital fijo

    # Creamos la instancia
    estrategia = Dalambert(cant_tiradas, cant_corridas,
                           numero_elegido, tipo_capital)

    # Ejecutamos la estrategia
    estrategia.ejecutar_estrategia()
