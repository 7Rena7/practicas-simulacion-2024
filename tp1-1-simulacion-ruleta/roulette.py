import random
import sys

# Verify if the correct number of arguments is provided in command line Six arguments must be provided: -c
# <num_tiradas> -n <num_corridas> -e <numero_elegido> All the arguments must be integers, -c must be between 1 and
# 1000, -n must be between 1 and 1000, and -e must be between 0 and 36
if len(sys.argv) != 7 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e":
    print("Uso: python/python3 roulette.py -c <cantidad_de_tiradas>[int] -n <cantidad_de_corridas>[int 00-36] -e "
          "<numero_elegido>[int]")
    sys.exit(1)

# Get the number of throws, runs, and the selected number from the command line arguments
num_throws = int(sys.argv[2])
num_runs = int(sys.argv[4])
number_selected = int(sys.argv[6])

if not (1 <= num_throws <= 1000):
    print("El número de tiradas debe estar entre 1 y 1000.")
    sys.exit(1)

if not (1 <= num_runs <= 1000):
    print("El número de corridas debe estar entre 1 y 1000.")
    sys.exit(1)

if not (0 <= number_selected <= 36):
    print("El número elegido debe estar entre 0 y 36.")
    sys.exit(1)

print("***** Simulación de una Ruleta con {} tiradas, {} corridas y con número {} *****\n"
      .format(num_throws, num_runs, number_selected))

# Generate random values between 0 and 36 and store them in a list
values = [random.randint(0, 36) for _ in range(num_throws)]
