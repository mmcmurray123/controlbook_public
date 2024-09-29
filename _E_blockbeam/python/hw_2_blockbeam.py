import matplotlib.pyplot as plt
import numpy as np
import blockbeamParam as P
from signalGenerator import signalGenerator
from blockbeamAnimation import blockbeamAnimation
from dataPlotter import dataPlotter


# instantiate reference input classes
reference = signalGenerator(amplitude=0.001, frequency=0.01)
zRef = signalGenerator(amplitude=-0.1, frequency=0.1, y_offset=P.length/2)
thetaRef = signalGenerator(amplitude=10*np.pi/180, frequency=0.1)
forceRef = signalGenerator(amplitude=2, frequency=0.1)



# instantiate the simulation plots and animation
dataPlot = dataPlotter()
animation = blockbeamAnimation()

t = P.t_start # time starts at this start
while t < P.t_end:
    # set variables
    z = zRef.sin(t)
    r = reference.sin(t)
    ctrl = forceRef.sin(t)
    theta = thetaRef.sin(t)
 

    # update animation

    state = np.array([[z],[theta]])
    animation.update(state)
    dataPlot.update(t, r, state, ctrl)

    # advance time by t_plot
    t = t + P.t_plot

    plt.pause(0.001) # allow time for animation to draw

    # Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()