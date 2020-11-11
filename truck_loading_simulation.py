"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A loading station has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the loading station at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they an use one.

"""
import random
import simpy


RANDOM_SEED = 42
NUM_LOADING = 2  # Number of loading stations
LOADINGTIME = 60      # Minutes it takes to clean a truck
T_INTER = 10       # Create a truck every ~ x hour
SIM_TIME = 1440     # Simulation time in minutes
DRIVETIME = 10      # Driving the truck to start the loading or exit the station

class Loadingtruck(object):
    """A lading has a limited number of loading stations (``NUM_LOADING``) to
    fill truck in parallel.

    Trucks have to request one of the loading stations. When they got one, they
    can start the loading processes and wait for it to finish (which
    takes ``loading time`` minutes).
    """
    def __init__(self, env, num_loading_station, loadingtime):
        self.env = env
        self.loadingstation = simpy.Resource(env, num_loading_station)
        self.loadingtime = loadingtime

    def filltruck(self, truck):
        """The loading processes. It takes a ``Truck`` processes and starts
        to fill it oil."""
        yield self.env.timeout(random.randint(LOADINGTIME-10, LOADINGTIME+10))
        # print("%s Truck start loading truck filled %d%% ." % (truck, random.randint(50, 99)))
        # print("%s start loading......" % (truck))

    def drivetrucktostation(self, truck):
        """The moving process to enter the truck to loading processes. It takes a ``truck`` processes and tries."""
        yield self.env.timeout(random.randint(DRIVETIME-5, DRIVETIME+5))
        # print("Drive %s to loading station......" % (truck))
        # print("Moving truck %s to loading station." % (truck))

def truck(env, name, cw):
    """The truck process (each truck has a ``name``) arrives at the loading stations
    (``cw``) and requests a cleaning loading station.

    It then starts the loading process, waits for it to finish and
    leaves to never come back ...

    """
    # print('%s arrives at the loading station at %.1f.' % (name, env.now))
    with cw.loadingstation.request() as request:
        yield request

        print('🚚....%s drives to loading station at %.1f hours.' % (name, env.now/60))
        yield env.process(cw.drivetrucktostation(name))

        print('%s Start loading process at %.1f hours. 🕓 ' % (name, env.now/60))
        yield env.process(cw.filltruck(name))

        # print('%s drives out from loading station at %.1f hours.' % (name, env.now/60))
        yield env.process(cw.drivetrucktostation(name))
        print('🏁.... %s left the loading station at %.1f hours.' % (name, env.now/60))


def setup(env, num_loading_station, loadingtime, t_inter):
    """Create a loading truck, a number of initial trucks and keep creating trucks
    approx. Every ``t_inter`` minutes."""
    # Create the loading truck
    loadingtruck = Loadingtruck(env, num_loading_station, loadingtime)

    # Create 4 initial trucks
    for i in range(4):
        env.process(truck(env, 'Truck %d' % i, loadingtruck))

    # Create more trucks while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 5, t_inter + 5))
        i += 1
        # i += num_loading_station
        env.process(truck(env, 'Truck %d' % i, loadingtruck))


# Setup and start the simulation
print('Loading truck Start')
# print('Check out http://youtu.be/fXXmeP9TvBg while simulating ... ;-)')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_LOADING, LOADINGTIME, T_INTER))

# Execute!
env.run(until=SIM_TIME)
