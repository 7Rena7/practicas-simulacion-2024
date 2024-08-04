import json
import numpy as np
import matplotlib.pyplot as plt

# Definición de variables globales
amount = 0
bigs = 0
initial_inv_level = 0
inv_level = 0
next_event_type = 0
num_events = 0
num_months = 0
num_values_demand = 0
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
    return np.random.exponential(mean)

def uniform(a, b):
    return np.random.uniform(a, b)

def random_integer(prob_distrib):
    u = np.random.rand()
    for i in range(1, len(prob_distrib)):
        if u < prob_distrib[i]:
            return i
    return len(prob_distrib)

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

def report():
    global area_holding, area_shortage, total_ordering_cost, num_months, smalls, bigs, holding_cost, shortage_cost
    # global final_tot, final_holding, final_shortage, final_ordering
    # global total_costs, ordering_costs, holding_costs, shortage_costs
    # global tot_per_pol, ord_per_pol, hold_per_pol, short_per_pol


    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months

    with open("inv.out.md", "a") as outfile:
        outfile.write(f"| ({smalls},{bigs}) | {avg_ordering_cost + avg_holding_cost + avg_shortage_cost:15.2f} |"
                        f" {avg_ordering_cost:15.2f} | {avg_holding_cost:15.2f} | {avg_shortage_cost:15.2f} |\n")

    print(f"({smalls},{bigs}){avg_ordering_cost + avg_holding_cost + avg_shortage_cost:15.2f}"
          f"{avg_ordering_cost:15.2f}{avg_holding_cost:15.2f}{avg_shortage_cost:15.2f}")


# def inventory_history_chart...

def cost_pie_chart(ordering_costs, holding_costs, shortage_costs, smallsArray, bigsArray):
    
    policies = []

    for small, big in zip(smallsArray, bigsArray):
        policy = f"Policy: {small}-{big}"
        policies.append(policy)
        policies = [...]

    # Creación de la figura y los ejes
    fig, ax = plt.subplots()

    # Creación del gráfico de torta
    labels = ['Ordering Cost', 'Holding Cost', 'Shortage Cost']
    sizes = [ordering_costs, holding_costs, shortage_costs]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    # Título de la gráfica
    ax.set_title('Costos finales')

    # Mostrar la gráfica
    plt.show()

def cost_per_policy_graphs(tot_per_pol, ord_per_pol, hold_per_pol, short_per_pol, smallsArray, bigsArray):
    policies = []

    for small, big in zip(smallsArray, bigsArray):
        policy = f"Policy: {small}-{big}"
        policies.append(policy)

    # Configuración de la gráfica de barras
    x = range(len(policies))
    width = 0.2              # Ancho de las barras

    # Creación de la figura y los ejes
    fig, ax = plt.subplots()

    # Creación de las barras para cada tipo de costo
    bar1 = ax.bar(x, tot_per_pol, width, label='Total Cost')
    bar2 = ax.bar([i + width for i in x], ord_per_pol, width, label='Ordering Cost')
    bar3 = ax.bar([i + 2*width for i in x], hold_per_pol, width, label='Holding Cost')
    bar4 = ax.bar([i + 3*width for i in x], short_per_pol, width, label='Shortage Cost')

    # Etiquetas de los ejes y título de la gráfica
    ax.set_xlabel('Políticas de inventario')
    ax.set_ylabel('Valor')
    ax.set_title('Desgloce de costos por política de inventario')
    ax.set_xticks([i + 1.5*width for i in x])
    ax.set_xticklabels(policies)

    # Leyenda de la gráfica
    ax.legend()

    # Mostrar la gráfica
    plt.show()



def update_time_avg_stats():
    global area_holding, area_shortage, time_last_event

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
    elif inv_level > 0:
        area_holding += inv_level * time_since_last_event

def timing():
    global sim_time, next_event_type

    next_event = min(time_next_event[1:5])
    next_event_type = time_next_event[1:5].index(next_event) + 1

    if next_event < sim_time:
        print(f"\nAttempt to schedule event type {next_event_type} for time {next_event} at time {sim_time}")
        exit(1)

    sim_time = next_event

def main():
    global initial_inv_level, num_months, num_values_demand, mean_interdemand
    global setup_cost, incremental_cost, holding_cost, shortage_cost, minlag
    global maxlag, prob_distrib_demand, num_events, smalls, bigs

    with open("inv_data.json", "r") as json_file, open("inv.out.md", "w") as outfile:
        data = json.load(json_file)

        num_events = 4
        initial_inv_level = data["initial_inv_level"]
        num_months = data["num_months"]
        num_policies = data["num_policies"]
        num_values_demand = data["num_values_demand"]
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
        outfile.write(f"**Number of demand sizes**: {num_values_demand}\n\n")
        outfile.write("**Distribution function of demand sizes**:  ")
        numbers = []
        for i in range(1, int(num_values_demand) + 1):
            numbers.append(str(prob_distrib_demand[i]))
        outfile.write("   ".join(numbers) + "\n\n")
        outfile.write(f"**Mean interdemand time**: {mean_interdemand:.2f} months\n\n")
        outfile.write(f"**Delivery lag range**: {minlag:.2f} to {maxlag:.2f} months\n\n")
        outfile.write(f"**Length of the simulation**: {num_months} months\n\n")
        outfile.write(f"K = {setup_cost:.1f}, i = {incremental_cost:.1f}, h = {holding_cost:.1f}, pi = {shortage_cost:.1f}\n\n")
        outfile.write(f"**Number of policies**: {num_policies}\n\n")
        outfile.write("| Policy | Average total cost | Average ordering cost | Average holding cost | Average shortage cost |\n")
        outfile.write("|--------|--------------------|-----------------------|----------------------|-----------------------|\n")


        for policy in policies:
            smalls = policy["smalls"]
            bigs = policy["bigs"]
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
                    report()
                # Inventory evaluation (and possible ordering) at the beginning of a month
                elif next_event_type == 4:
                    evaluate()
                
                if next_event_type == 3:
                    break
   


    cost_pie_chart(final_ordering, final_holding, final_shortage, smallsArray, bigsArray)
    cost_per_policy_graphs(tot_per_pol, ord_per_pol, hold_per_pol, short_per_pol, smallsArray, bigsArray)
    # este
        # print("\n\n" + "\033[4m" + "Final costs" + "\033[0m")
        # print("Total cost:", round(final_tot, 2))
        # print("Ordering cost:", round(final_ordering, 2))
        # print("Holding cost:", round(final_holding, 2))
        # print("Shortage cost:", round(final_shortage, 2))

if __name__ == "__main__":
    main()
