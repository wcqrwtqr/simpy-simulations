import simpy
import numpy as np

STORAGE_TANK_SIZE = 79500 # Litters of the tank 500 bbls
FLOW_RATE = 4500 # Litter per minute (x9 to get the bbl/day)
DRAIN_RATE = 700 # Litter per minute (x9 to get the bbl/day)
is_empty = True


# This is the good code
def flowing_well_to_tanks(env, tanks):
    i = 0
    while True:
        i += 1
        if is_empty == True: 
            yield env.process(filling_tank(env,i, tanks))
        yield env.process(draining_tank(env,i, tanks))
        #TODO there is an issue of the tanks must wait until the tank is empty
        #Find a solution for this in the code above

# The filling process for the tank
def filling_tank(env,name, tanks):
    with tanks.request() as request:
        yield request
        print('start filling tank No. {} at {:.2f}'.format(name,env.now))
        yield env.timeout(np.random.randint(3,7))
        yield env.timeout(generate_filling_time())
        yield env.timeout(np.random.randint(3,7))
        print('finish filling tank No.{} at {:.2f}'.format(name, env.now))
        is_empty = False

#The dumping and draining process
def draining_tank(env,name, tanks):
    with tanks.request() as request:
        yield request
        print('start draining tanks No. {} at {:.2f}'.format(name,env.now))
        yield env.timeout(np.random.randint(3,7))
        yield env.timeout(generate_drain_time())
        yield env.timeout(np.random.randint(3,7))
        print('finish draining tank No. {} at {:.2f}'.format(name, env.now))
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




