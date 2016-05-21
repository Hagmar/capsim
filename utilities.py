import random

def inter_arrival_sequence(n=None):
    if n:
        for _ in range(n):
            yield inter_arrival_time()
    else:
        while True:
            yield inter_arrival_time()

def inter_arrival_time():
    a1 = random.expovariate(0.85)
    a2 = random.uniform(0.05, 0.25)
    return a1+a2

def pre_processor_service_time(n):
    return random.expovariate(10/n)

def sub_task_service_time(n):
    k0 = 20*(1.08/2.08)/pow(n, 1.65)
    return random.paretovariate(2.08)*k0
