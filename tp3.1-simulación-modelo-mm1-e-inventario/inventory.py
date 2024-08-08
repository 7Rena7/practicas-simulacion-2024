import json
import numpy as np
import matplotlib.pyplot as plt
import math
import random

# Definición de variables globales
amount = 0
bigs = 0
initial_inv_level = 0
inv_level = 0
next_event_type = 0
num_events = 0
num_months = 0
smalls = 0
area_holding = 0.0
area_shortage = 0.0
holding_cost = 0.0
incremental_cost = 0.0
maxlag = 0.0
mean_interdemand = 0.0
minlag = 0.0
prob_distrib_demand = [0.0] * 26
setup_cost = 0.0
shortage_cost = 0.0
sim_time = 0.0
time_last_event = 0.0
time_next_event = [0.0] * 5

# costs
total_ordering_cost = 0.0
final_tot = 0.0
final_holding = 0.0
final_shortage = 0.0
final_ordering = 0.0

total_costs = []
ordering_costs = []
holding_costs = []
shortage_costs = []
tot_per_pol = []
ord_per_pol = []
hold_per_pol = []
short_per_pol = []


total_costs_per_run = []
ordering_costs_per_run = []
holding_costs_per_run = []
shortage_costs_per_run = []
tot_per_pol_per_run = []
ord_per_pol_per_run = []
hold_per_pol_per_run = []
short_per_pol_per_run = []



def initialize():
    global sim_time, inv_level, time_last_event, total_ordering_cost
    global area_holding, area_shortage, time_next_event

    sim_time = 0.0
    inv_level = initial_inv_level
    time_last_event = 0.0
    total_ordering_cost = 0.0
    area_holding = 0.0
    area_shortage = 0.0
    time_next_event[1] = 1.0e+30
    time_next_event[2] = sim_time + expon(mean_interdemand)
    time_next_event[3] = num_months
    time_next_event[4] = 0.0

def expon(mean): 
    return -mean * math.log(random.random())

def uniform(a, b):
    return a + random.random() * (b - a)

def random_integer(prob_distrib):
    u = random.random()

    # Retorna un entero aleatorio de acuerdo con la función de distribución acumulativa "prob_distrib"
    i = 1
    while u >= prob_distrib[i]:
        i += 1
    return i

def order_arrival():
    global inv_level, amount, time_next_event

    inv_level += amount
    time_next_event[1] = 1.0e+30

def demand():
    global inv_level, time_next_event

    inv_level -= random_integer(prob_distrib_demand)
    time_next_event[2] = sim_time + expon(mean_interdemand)

def evaluate():
    global inv_level, amount, total_ordering_cost, time_next_event

    if inv_level < smalls:
        amount = bigs - inv_level
        total_ordering_cost += setup_cost + incremental_cost * amount
        time_next_event[1] = sim_time + uniform(minlag, maxlag)
    time_next_event[4] = sim_time + 1.0

def report(outfile):
    global area_holding, area_shortage, total_ordering_cost, num_months, smalls, bigs, holding_cost, shortage_cost

    global final_tot, final_holding, final_shortage, final_ordering
    global total_costs, ordering_costs, holding_costs, shortage_costs
    global tot_per_pol, ord_per_pol, hold_per_pol, short_per_pol

    # Calcula y devuelve estimaciones de medidas deseadas de rendimiento.
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months
    avg_ordering_cost = total_ordering_cost / num_months

    # Suma el acumulado total
    final_tot += avg_holding_cost + avg_shortage_cost + avg_ordering_cost
    final_holding += avg_holding_cost
    final_shortage += avg_shortage_cost
    final_ordering += avg_ordering_cost

    tot_per_pol.append(avg_holding_cost + avg_shortage_cost + avg_ordering_cost)
    ord_per_pol.append(avg_ordering_cost)
    hold_per_pol.append(avg_holding_cost)
    short_per_pol.append(avg_shortage_cost)

    total_costs.append(avg_holding_cost + avg_shortage_cost + avg_ordering_cost)
    ordering_costs.append(avg_ordering_cost)
    holding_costs.append(avg_holding_cost)
    shortage_costs.append(avg_shortage_cost)


    outfile.write(f"| ({smalls},{bigs}) | {avg_ordering_cost + avg_holding_cost + avg_shortage_cost:15.2f} |"
                    f" {avg_ordering_cost:15.2f} | {avg_holding_cost:15.2f} | {avg_shortage_cost:15.2f} |\n")

   

# def inventory_history_chart...

def calculate_costs():
    pass

def cost_pie_chart(ordering_cost, holding_cost, shortage_cost, policy):
    # Creación de la figura y los ejes
    fig, ax = plt.subplots()

    # Colores personalizados para que coincidan con la gráfica de pastel
    colors = ['#FFDD44', '#A4D144', '#FF4444']  # Amarillo, Verde, Rojo

    # Creación del gráfico de torta
    labels = ['Costo por pedido', 'Costo de mantenimiento', 'Costo por faltante']
    sizes = [ordering_cost, holding_cost, shortage_cost]
    total_cost = sum(sizes)
    autopct = lambda p: f'{p:.1f}%\n({p * total_cost / 100:.2f})'

    ax.pie(sizes, labels=labels, colors=colors, autopct=autopct, startangle=90)

    # Título de la gráfica
    ax.set_title(f'Costos finales para la política {policy}')

    # Guardar la gráfica
    plt.savefig(f'./inventory-images/{policy}_python.png')
    plt.close()


def cost_per_policy_graphs(tot_per_pol, ord_per_pol, hold_per_pol, short_per_pol, smallsArray, bigsArray):
    policies = []

    for small, big in zip(smallsArray, bigsArray):
        policy = f"{small}-{big}"
        policies.append(policy)

    # Configuración de la gráfica de barras
    x = range(len(policies))
    width = 0.2  # Ancho de las barras

    # Creación de la figura y los ejes
    fig, ax = plt.subplots()

    # Colores personalizados para que coincidan con la gráfica de pastel
    color_order = '#FFDD44'  # Amarillo
    color_maintenance = '#A4D144'  # Verde
    color_shortage = '#FF4444'  # Rojo

    # Creación de las barras para cada tipo de costo con los colores especificados
    ax.bar(x, tot_per_pol, width, label='Costo Total', color='lightblue')
    ax.bar([i + width for i in x], ord_per_pol, width, label='Costo por pedido', color=color_order)
    ax.bar([i + 2*width for i in x], hold_per_pol, width, label='Costo por mantenimiento', color=color_maintenance)
    ax.bar([i + 3*width for i in x], short_per_pol, width, label='Costo por faltante', color=color_shortage)

    # Etiquetas de los ejes y título de la gráfica
    ax.set_xlabel('Políticas de inventario')
    ax.set_ylabel('Valor')
    ax.set_title('Costos por política de inventario')
    ax.set_xticks([i + 1.5*width for i in x])
    ax.set_xticklabels(policies)

    # Leyenda de la gráfica
    ax.legend()

    # Mostrar la gráfica
    plt.show()
 

def update_time_avg_stats():
    global sim_time, time_last_event, inv_level, area_shortage, area_holding
 
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

 
    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
    elif inv_level > 0:
        area_holding += inv_level * time_since_last_event


def timing():
    global sim_time, next_event_type, time_next_event, num_events

    # Determina el siguiente tipo de evento y avanza el reloj de simulación
    min_time_next_event = 1.0e+30
    next_event_type = 0
    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i
        
    if next_event_type == 0:
        print("Event list empty at time {}".format(sim_time))
        exit(1)

    sim_time = min_time_next_event

def main():
    global initial_inv_level, num_months, mean_interdemand
    global setup_cost, incremental_cost, holding_cost, shortage_cost, minlag
    global maxlag, prob_distrib_demand, num_events, smalls, bigs

    with open("inv_data.json", "r") as json_file, open("readme.md", "w") as outfile:
        data = json.load(json_file)

        num_events = 4
        initial_inv_level = data["initial_inv_level"]
        num_months = data["num_months"]
        mean_interdemand = data["mean_interdemand"]
        setup_cost = data["setup_cost"]
        incremental_cost = data["incremental_cost"]
        holding_cost = data["holding_cost"]
        shortage_cost = data["shortage_cost"]
        minlag = data["minlag"]
        maxlag = data["maxlag"]

        prob_distrib_demand = data["prob_distrib_demand"]
        policies = data["policies"]

        outfile.write("# Single-product inventory system\n\n")
        outfile.write(f"**Initial inventory level**: {initial_inv_level} items\n\n")
        outfile.write(f"**Number of demand sizes**: {len(prob_distrib_demand)}\n\n")  
        outfile.write("**Distribution function of demand sizes**:  "+" ".join([str(prob_distr) for prob_distr in prob_distrib_demand])+"\n\n")
        outfile.write(f"**Mean interdemand time**: {mean_interdemand:.2f} months\n\n")
        outfile.write(f"**Delivery lag range**: {minlag:.2f} to {maxlag:.2f} months\n\n")
        outfile.write(f"**Length of the simulation**: {num_months} months\n\n")
        outfile.write(f"K = {setup_cost:.1f}, i = {incremental_cost:.1f}, h = {holding_cost:.1f}, pi = {shortage_cost:.1f}\n\n")
        outfile.write(f"**Number of policies**: {len(policies)}\n\n")
        outfile.write("| Policy | Average total cost | Average ordering cost | Average holding cost | Average shortage cost |\n")
        outfile.write("|--------|--------------------|-----------------------|----------------------|-----------------------|\n")

        smallsArray = []
        bigsArray = []

        for policy in policies:
            # for i in range (1,10):
            #     pass
            smalls = policy["smalls"]
            bigs = policy["bigs"]
            smallsArray.append(smalls)
            print(smalls,bigs)
            bigsArray.append(bigs)
            initialize()
 
            while True:
                timing()
                update_time_avg_stats()

                # Arrival of an order to the company from the supplier
                if next_event_type == 1:
                    order_arrival()
                # Demand for the product from a customer
                elif next_event_type == 2:
                    demand()
                # End of the simulation after n months
                elif next_event_type == 3:
                    calculate_costs()
                    report(outfile)
                    break
                # Inventory evaluation (and possible ordering) at the beginning of a month
                elif next_event_type == 4:
                    evaluate()


    with open("readme.md", "a") as outfile:
        outfile.write(f"| **Total** | {round(final_tot, 2)} |{round(final_ordering, 2)} | {round(final_holding, 2)} | {round(final_shortage, 2)} |\n")


                
    cost_pie_chart(final_ordering, final_holding, final_shortage, smallsArray, bigsArray)
    cost_per_policy_graphs(tot_per_pol, ord_per_pol, hold_per_pol, short_per_pol, smallsArray, bigsArray)
 
if __name__ == "__main__":
    main()