import itertools
import random
import simpy
import numpy as np


import time

contador = 10
cou_ocupado = False

RANDOM_SEED = 42
I_MAX = 3  # Instrucciones maximas por unidad de tiempo
TIME = 1      # Tiempo en el que se atiende un proceso
T_INTER = 10       # intervalo de creacion de procesos
NUM_PROCESOS = 25    # numero de procrsos

start_times = []
end_times = []
random.seed(RANDOM_SEED)
env = simpy.Environment()

RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity = 1)

def generator(env):
    process_count = 0

    while process_count < NUM_PROCESOS: 
        env.process(new(env, f'Proceso {process_count}'))
        process_count += 1
        yield env.timeout(random.expovariate(1.0 / T_INTER))
        

def new(env, num):
    RAM_process = random.randint(1, 10)
    print(f'Proceso {num} solicita {RAM_process} de RAM en {env.now:.2f}.')
    start_times.append(env.now)

    yield(RAM.get(RAM_process))

    print(f'Proceso {num} con {RAM_process} de RAM pasa a ready en {env.now:.2f}')

    env.process(ready(env, num, RAM_process))





def terminated(env, num, RAM_process):
    yield RAM.put(RAM_process)
    print(f'Proceso {num} ha terminado en {env.now:.2f}.')
    end_times.append(env.now)


def waiting(env, num, RAM_process):
    yield env.timeout(random.randint(1, 5))  
    print(f'Proceso {num} esta en waiting en {env.now:.2f}.')
    
    env.process(ready(env, num, RAM_process))
    print(f'Proceso {num} regresa a ready en {env.now:.2f}.')


env.process(generator(env, NUM_PROCESOS))

t_total: [end - start for start, end in zip(start_times, end_times)]
t_prom = np.mean(t_total)
t_desv = np.std(t_total)

print(f"Tiempo promedio: {t_prom:.2f}")
print(f"Desviación estándar: {t_desv:.2f}")

env.run(until=100)

def ready():
    global cou_ocupado
    print("[READY] Esperando que el cou esté desocupado...")
    while cou_ocupado:
        time.sleep(1)  
    print("[READY] cou desocupado, pasando al estado RUNNING")
    running()

def running():
    global contador, cou_ocupado
    cou_ocupado = True
    print(f"[RUNNING] Iniciando ejecución. Contador actual: {contador}")

 
    contador -= 3
    time.sleep(1)  

    if contador <= 0:
        print("[RUNNING] Proceso terminado (contador = 0)")
        cou_ocupado = False
    else:
        siguiente_estado = random.randint(1, 2)
        print(f"[RUNNING] Proceso incompleto. Contador restante: {contador}")
        if siguiente_estado == 1:
            print("[RUNNING] Enviando de nuevo al estado READY")
            cou_ocupado = False
            ready() 
        else:
            print("[RUNNING] Enviando al estado WAITING")
            waiting()


def waiting():
    global cou_ocupado
    print("[WAITING] Esperando un momento antes de volver a READY...")
    time.sleep(2)  # Simular espera
    cou_ocupado = False
    ready()  

ready()




    