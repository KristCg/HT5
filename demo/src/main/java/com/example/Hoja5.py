import itertools
import random

import simpy



RANDOM_SEED = 42
I_MAX = 3  # Instrucciones maximas por unidad de tiempo
TIME = 1      # Tiempo en el que se atiende un proceso
T_INTER = 10       # intervalo de creacion de procesos
NUM_PROCESOS = 25    # numero de procrsos


random.seed(RANDOM_SEED)
env = simpy.Environment()

RAM = simpy.Container(env, init=100, capacity=100)

def generator(env):
    process_count = 0

    while True:
        env.process(new(env, f'Proceso {process_count}'))
        process_count += 1
        yield env.timeout(10)
        

def new(env, num):
    RAM_process = random.randint(1, 10)
    print(f'Proceso {num} solicita {RAM_process} de RAM en {env.now:.2f}.')

    yield(RAM.get(RAM_process))

    print(f'Proceso {num} pasa a ready en {env.now:.2f}')




    