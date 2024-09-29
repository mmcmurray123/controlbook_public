# VTOL Parameter File
import numpy as np

# Physical parameters of the  VTOL known to the controller
mc = 1 # kg
mr =  0.25 # kg
Jc =  0.0042 # kg m^2
d =  0.3 # m
mu = 0.1  # kg/s
g =  9.81 # m/s^2
F_wind =  0# wind disturbance force is zero in initial homeworks

# parameters for animation
length = 10.0

# Initial Conditions
z0 =  1 # initial lateral position
h0 = 10  # initial altitude
theta0 = 1 * np.pi/180 # initial roll angle
zdot0 = 1 # initial lateral velocity
hdot0 = 1  # initial climb rate
thetadot0 =  1 * np.pi/180 # initial roll rate
target0 = 10

# Simulation Parameters
t_start = 0.0  # Start time of simulation
t_end = 50.0  # End time of simulation
Ts = 0.01  # sample time for simulation
t_plot = 0.1  # the plotting and animation is updated at this rate

# saturation limits
fmax = 100  # Max Force, N

# dirty derivative parameters
# sigma =   # cutoff freq for dirty derivative
# beta =  # dirty derivative gain

# equilibrium force
# Fe =

# mixing matrix
unmixing = np.array([[1.0, 1.0], [d, -d]]) # converts fl and fr (LR) to force and torque (FT)
mixing = np.linalg.inv(unmixing) # converts force and torque (FT) to fl and fr (LR) 

