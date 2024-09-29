import matplotlib.pyplot as plt
import VTOLParam as P
from signalGenerator import signalGenerator
from VTOLAnimation import VTOLAnimation
from dataPlotter import dataPlotter
from VTOLDynamics import Dynamics
import numpy as np

# instantiate mass, controller, and reference classes
vtol = Dynamics()
#second_vtol = Dynamics()
reference = signalGenerator(amplitude=0.01, frequency=0.02)
force = signalGenerator(amplitude=1, frequency=1, y_offset=1.5)
#force2 = signalGenerator(amplitude=0.1, frequency=0.01)

# instantiate the simulation plots and animation
dataPlot = dataPlotter()
#dataPlot2 = dataPlotter()
animation = VTOLAnimation()
#animation2 = VTOLAnimation()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    # updates control and dynamics at faster simulation rate
    while t < t_next_plot:  
        # Get referenced inputs from signal generators
        r = reference.square(t)
        u = np.array([[force.sin(t)],[force.sin(t)]])
        #u2 = force2.sin(t)
        y = vtol.update(u)  # Propagate the dynamics
        #y2 = second_mass.update(u2)
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.update(vtol.state)
    #animation2.update(second_vtol.state)
    dataPlot.update(t, vtol.state, r, r, u[0][0], P.d * (u[1][0] - u[0][0]))
    #dataPlot2.update(t, r, second_vtol.state, u2)

    # the pause causes the figure to be displayed during the
    # simulation
    plt.pause(0.0001)  

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
