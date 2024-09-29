import numpy as np 
import blockbeamParam as P


class blockbeamDynamics:
    def __init__(self, alpha=0.0):
        # Initial state conditions
        self.state = np.array([
            [P.z0],      # initial z
            [P.theta0],      # initial angle
            [P.zdot0],    # initial time z-velocity
            [P.thetadot0],    # initial angular velocity
        ])  
        # Mass of the block
        self.m1 = P.m1 * (1.+alpha*(2.*np.random.rand()-1.))
        # Mass of the beam
        self.m2 = P.m2 * (1.+alpha*(2.*np.random.rand()-1.))
        # the gravity constant is well known, so we don't change it.
        self.g = P.g
        # length of the beam
        self.length = P.length

        # sample rate at which the dynamics are propagated
        self.Ts = P.Ts  
        self.force_limit = P.Fmax

    def update(self, u):
        # This is the external method that takes the input u at time
        # t and returns the output y at time t.
        # saturate the input force
        u = saturate(u, self.force_limit)
        self.rk4_step(u)  # propagate the state by one time sample
        y = self.h()  # return the corresponding output
        return y

    def f(self, state, F):
        # Return xdot = f(x,u), the system state update equations
        # re-label states for readability
        z = state[0][0]
        theta = state[1][0]
        zdot = state[2][0]
        thetadot = state[3][0]
        
        zddot = -self.g*np.sin(theta) + z*thetadot**2
        thetaddot = (F*self.length*np.cos(theta) \
                    - (1/2)*self.length*self.g*self.m2*np.cos(theta) \
                    - self.g*self.m1*z*np.cos(theta) \
                    - 2*self.m1*z*zdot*thetadot) / \
                    ((self.length**2*self.m2/3) + self.m1*z**2)

        xdot = np.array([[zdot], [thetadot],[zddot],[thetaddot]])
        return xdot

    def h(self):
        # return the output equations
        # could also use input u if needed
        z = self.state[0][0]
        theta = self.state[1][0]
        y = np.array([[z],[theta]])
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
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u
