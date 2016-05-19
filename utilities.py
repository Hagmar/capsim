import random

def inter_arrival_sequence(n=None):
    if n:
        for _ in range(n):
            yield inter_arrival_time()
    else:
        while True:
            yield inter_arrival_time()

def inter_arrival_time():
    a1 = random.expovariate(1/0.85)
    a2 = random.uniform(0.05, 0.25)
    return a1+a2
