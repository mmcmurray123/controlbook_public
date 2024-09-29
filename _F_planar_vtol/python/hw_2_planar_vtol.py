import matplotlib.pyplot as plt
import numpy as np
import VTOLParam as P
from signalGenerator import signalGenerator
from VTOLAnimation import VTOLAnimation
from dataPlotter import dataPlotter


# instantiate reference input classes
z_reference = signalGenerator(amplitude=0.001, frequency=0.01)
h_reference = signalGenerator(amplitude=0.001, frequency=0.01)
z_reference = signalGenerator(amplitude=0.001, frequency=0.01)
zRef = signalGenerator(amplitude=4, frequency=0.1, y_offset=P.length/2)
hRef = signalGenerator(amplitude=2, frequency=0.1, y_offset=P.length/2)
thetaRef = signalGenerator(amplitude=45*np.pi/180, frequency=0.1)
forceRef = signalGenerator(amplitude=2, frequency=0.1)
torqueRef = signalGenerator(amplitude=2, frequency=0.1)




# instantiate the simulation plots and animation
dataPlot = dataPlotter()
animation = VTOLAnimation()

t = P.t_start # time starts at this start
while t < P.t_end:
    # set variables
    z = zRef.sin(t)
    h = hRef.sin(t)
    z_ref = z_reference.sin(t)
    h_ref = h_reference.sin(t)
    ctrl = forceRef.sin(t)
    theta = thetaRef.sin(t)
    torque = torqueRef.sin(t)
 

    # update animation

    state = np.array([[z],[h],[theta]])
    animation.update(state)
    dataPlot.update(t, state, z_ref, h_ref, ctrl, torque)

    # advance time by t_plot
    t = t + P.t_plot

    plt.pause(0.001) # allow time for animation to draw

    # Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()