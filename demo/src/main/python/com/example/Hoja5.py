import random
import simpy
import numpy as np
import time

# Parámetros de la simulación
RANDOM_SEED = 42
I_MAX = 3  # Instrucciones máximas por unidad de tiempo
TIME = 1  # Tiempo en el que se atiende un proceso
T_INTER = 10  # Intervalo de creación de procesos
NUM_PROCESOS = 25  # Número de procesos

start = []
end = []
random.seed(RANDOM_SEED)

env = simpy.Environment()

RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)

def generator(env):
    process_count = 0

    while process_count < NUM_PROCESOS:
        env.process(new(env, f'Proceso {process_count}'))
        process_count += 1
        yield env.timeout(random.expovariate(1.0 / T_INTER))

def new(env, num):
    RAM_process = random.randint(1, 10)  
    print(f'Proceso {num} solicita {RAM_process} de RAM en {env.now:.2f}.')
    start.append(env.now)  

    yield RAM.get(RAM_process)

    print(f'Proceso {num} con {RAM_process} de RAM pasa a ready en {env.now:.2f}')
    env.process(ready(env, num, RAM_process))  

def terminated(env, num, RAM_process):
    yield RAM.put(RAM_process)
    print(f'Proceso {num} ha terminado en {env.now:.2f}.')
    end.append(env.now)  

def ready(env, num, RAM_process):
    print(f"[READY] Proceso {num} esperando que el CPU esté desocupado...")
    with CPU.request() as req:
        yield req  
        print(f"[READY] CPU desocupado, Proceso {num} pasando al estado RUNNING")
        yield env.process(running(env, num, RAM_process))  

def running(env, num, RAM_process):
    contador = random.randint(1, 10)  
    print(f"[RUNNING] Proceso {num} iniciando ejecución. Contador actual: {contador}")

    contador -= I_MAX
    yield env.timeout(TIME)  

    if contador <= 0:
        print(f"[RUNNING] Proceso {num} terminado (contador = 0)")
        yield env.process(terminated(env, num, RAM_process))  

        siguiente_estado = random.randint(1, 2)
        print(f"[RUNNING] Proceso {num} incompleto. Contador restante: {contador}")
        if siguiente_estado == 1:
            print(f"[RUNNING] Proceso {num} enviando de nuevo al estado READY")
            yield env.process(ready(env, num, RAM_process))  
        else:
            print(f"[RUNNING] Proceso {num} enviando al estado WAITING")
            yield env.process(waiting(env, num, RAM_process)) 

def waiting(env, num, RAM_process):
    print(f"[WAITING] Proceso {num} esperando un momento antes de volver a READY...")
    yield env.timeout(2)  
    print(f"[WAITING] Proceso {num} volviendo al estado READY")
    yield env.process(ready(env, num, RAM_process)) 

env.process(generator(env))
env.run(until=200)  


t_prom_start = np.mean(start)
t_prom_end = np.mean(end)
t_prom = t_prom_end - t_prom_start

t_desv_start = np.std(start)
t_desv_end = np.std(end)
t_desv = t_desv_end - t_desv_start

print(t_prom)
print(t_desv)
