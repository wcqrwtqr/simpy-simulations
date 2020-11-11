import simpy
import numpy as np

STORAGE_TANK_SIZE = 79500 # Litters of the tank 500 bbls
FLOW_RATE = 1500 # Litter per minute (x9 to get the bbl/day)
DRAIN_RATE = 1000 # Litter per minute (x9 to get the bbl/day)
is_empty = True


# This is the good code
def flowing_well_to_tanks(env, tanks):
    i = 0
    while True:
        i += 1
        if is_empty == True: 
            yield env.process(filling_tank(env,i, tanks))
        yield env.process(draining_tank(env,i, tanks))
def filling_tank(env,name, tanks):
    with tanks.request() as request:
        yield request
        print('start filling count {} at {:.2f}'.format(name,env.now))
        yield env.timeout(np.random.randint(3,7))
        yield env.timeout(generate_filling_time())
        yield env.timeout(np.random.randint(3,7))
        print('finish filling at {:.2f}'.format(env.now))
        is_empty = False


def draining_tank(env,name, tanks):
    with tanks.request() as request:
        yield request
        print('start draining count {} at {:.2f}'.format(name,env.now))
        yield env.timeout(np.random.randint(3,7))
        yield env.timeout(generate_drain_time())
        yield env.timeout(np.random.randint(3,7))
        print('finish draining at {:.2f}'.format(env.now))
        is_empty = True

#======================================

def generate_filling_time():
    fill_time = STORAGE_TANK_SIZE / FLOW_RATE
    return fill_time


def generate_drain_time():
    drain_time = STORAGE_TANK_SIZE / DRAIN_RATE
    return drain_time

env = simpy.Environment()
tanks = simpy.Resource(env, capacity=8)
env.process(flowing_well_to_tanks(env, tanks))
np.random.seed(5)
env.run(until=1440)




