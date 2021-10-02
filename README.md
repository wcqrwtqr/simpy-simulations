# simpy-simulations
Simpy simulation with python

This script is used to play with simpy framework to model actions such as ability to serve customers in a cinema and other places which I used to apply it to storage tanks filling for the oil field operation.

- The script is used prefilled with initial values of the following:
	- Time of filling a full truck
	- Time of driving the truck into and out from the station
	- Number of loading stations available
	- The time of loading (day and night operation or day operation only)
- The user can change the values from within the code to the his own preference and simulate the operation accordingly

To run the simulation ensure to have the simpy framework installed using pip like below and run the command for the simulation to start

```bash
pip install simpy

python3 truck_loading_simulation.py
```
To get the output sent to a file in your preferred path use the folling command and use the >> to ensure the values are being appended so you can get more simulation in the same file and can compare between features easly

```bash
python3 truck_loading_simulation.py >> /tmp/simpy
```
The file simpy (you can choose the file name and location you like) will get the results of the simulation 
