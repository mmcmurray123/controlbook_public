import numpy as np 
import VTOLParam as P


class Dynamics:
    def __init__(self, alpha=0.0):
        # Initial state conditions
        self.state = np.array([
            [P.z0],      # initial z
            [P.h0],
            [P.theta0],      # initial angle
            [P.zdot0],    # initial time z-velocity
            [P.hdot0],
            [P.thetadot0],    # initial angular velocity
        ])  
        # Mass of the block
        self.mc = P.mc * (1.+alpha*(2.*np.random.rand()-1.))
        # Mass of the beam
        self.mr = P.mr * (1.+alpha*(2.*np.random.rand()-1.))
        # the gravity constant is well known, so we don't change it.
        self.g = P.g
        # wing length
        self.d = P.d
        # drag 
        self.mu = P.mu
        # F_wind
        self.F_wind = P.F_wind
        # moment
        self.Jc = P.Jc

        # sample rate at which the dynamics are propagated
        self.Ts = P.Ts  
        self.force_limit = P.fmax

    def update(self, u):
        # This is the external method that takes the input u at time
        # t and returns the output y at time t.
        # saturate the input force
        u = saturate(u, self.force_limit)
        self.rk4_step(u)  # propagate the state by one time sample
        y = self.h()  # return the corresponding output
        return y

    def f(self, state, tau):
        # Return xdot = f(x,u), the system state update equations
        # re-label states for readability
        fr = tau[0][0]
        fl = tau[1][0]
        z = state[0][0]
        h = state[1][0]
        theta = state[2][0]
        zdot = state[3][0]
        hdot = state[4][0]
        thetadot = state[5][0]
        
        zddot = (-self.mu*zdot-(fl+fr)*np.sin(theta)) / (self.mc + 2*self.mr)
        hddot = ((fl+fr)*np.cos(theta) - self.g*self.mc - 2*self.g*self.mr) / (self.mc + 2.0*self.mr)
        thetaddot = self.d*(fr-fl) / (self.Jc + 2.0*self.d**2*self.mr)
        

        xdot = np.array([[zdot], [hdot],[thetadot],[zddot],[hddot],[thetaddot]])
        return xdot

    def h(self):
        # return the output equations
        # could also use input u if needed
        z = self.state[0][0]
        h = self.state[1][0]
        theta = self.state[2][0]
        y = np.array([[z],[h],[theta]])
        return y

    def rk4_step(self, u):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        self.state = self.state.astype(float)
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + self.Ts / 2 * F1, u)
        F3 = self.f(self.state + self.Ts / 2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

    
def saturate(u, limit):
    if abs(u[1][0]) > limit:
        u = limit * np.sign(u)
    elif abs(u[0][0]) > limit:
        u = limit * np.sign(u)
    return u
