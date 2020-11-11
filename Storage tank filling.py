import random
import simpy

RANDOM_SEED = 42
STORAGE_TANK_SIZE = 79500     # liters
# THRESHOLD = 10             # Threshold for calling the tank truck (in %)
# FUEL_TANK_SIZE = 30000        # liters
STORAGE_TANK_LEVEL = [8000, 70000]  # Min/max levels of fuel tanks (in liters)
FLOW_SPEED = 795000        # liters / day
DRAIN_SPEED = 795000        # liters / day
# TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
# T_INTER = [5,20]        # Create a car every [min, max] seconds
SIM_TIME = 86000            # Simulation time in seconds
is_filling = True


class Tanks(object):
    def __init__(self,env,num_tanks):
        self.env  = env
        self.num_tanks = simpy.Resource(env,num_tanks)

    def fill_tank_timing(self,flow_speed):
        fill_time = STORAGE_TANK_SIZE/(FLOW_SPEED/1440)
        yield self.env.timeout(fill_time)

    def drain_tank_timing(self,drain_speed):
        drain_time = STORAGE_TANK_SIZE/(DRAIN_SPEED/1440)
        yield self.env.timeout(fill_time)

def filling_tank(env,tanks,flow_speed):
    start_filling_time = env.now
    is_filling = True
    with tanks.num_tanks.request() as request:
        yield request
        yield env.process(tanks.fill_tank_timing(flow_speed))
    

def main():

    env = simpy.Environment()
    env.process(filling_tank(env,2,FLOW_SPEED))
    env.run(until=144)
    print ('test')

if __name__ == '__main__':
    main()





