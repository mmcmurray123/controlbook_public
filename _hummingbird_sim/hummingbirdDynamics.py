import numpy as np 
import hummingbirdParam as P


class HummingbirdDynamics:
    def __init__(self, alpha=0.0):
        # Initial state conditions
        self.state = np.array([
            [P.phi0],  # roll angle
            [P.theta0],  # pitch angle
            [P.psi0],  # yaw angle
            [P.phi0],  # roll rate
            [P.thetadot0],  # pitch rate
            [P.psidot0],  # yaw rate
        ])

        # vary the actual physical parameters
        self.ell1 = P.ell1 * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell2 = P.ell2 * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell3x = P.ell3x * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell3y = P.ell3y * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell3z = P.ell3z * (1.+alpha*(2.*np.random.rand()-1.))
        self.ellT = P.ellT * (1.+alpha*(2.*np.random.rand()-1.))
        self.d = P.d * (1.+alpha*(2.*np.random.rand()-1.))
        self.m1 = P.m1 * (1.+alpha*(2.*np.random.rand()-1.))
        self.m2 = P.m2 * (1.+alpha*(2.*np.random.rand()-1.))
        self.m3 = P.m3 * (1.+alpha*(2.*np.random.rand()-1.))
        self.J1x = P.J1x * (1.+alpha*(2.*np.random.rand()-1.))
        self.J1y = P.J1y * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J1z = P.J1z * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J2x = P.J2x * (1.+alpha*(2.*np.random.rand()-1.))
        self.J2y = P.J2y * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J2z = P.J2z * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J3x = P.J3x * (1.+alpha*(2.*np.random.rand()-1.))
        self.J3y = P.J3y * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J3z = P.J3z * (1. + alpha * (2. * np.random.rand() - 1.))
 
    def update(self, u):
        # This is the external method that takes the input u at time
        # t and returns the output y at time t.
        # saturate the input force
        u = saturate(u, P.torque_max)
        self.rk4_step(u)  # propagate the state by one time sample
        y = self.h()  # return the corresponding output
        return y

    def f(self, state, u):
        # Return xdot = f(x,u)
        phi = state[0][0]
        theta = state[1][0]
        psi = state[2][0]
        phidot = state[3][0]
        thetadot = state[4][0]
        psidot = state[5][0]
        pwm_left = u[0][0]
        pwm_right = u[1][0]
        # The equations of motion go here
        M22 = self.m1*self.ell1**2+ \
            self.m2*self.ell2**2 \
                +self.J2y+ \
                    self.J1y*np.cos(phi)**2 \
                    +self.J1z*np.sin(phi)**2
        M23 = (self.J1y-self.J1z)*np.sin(phi)*np.cos(phi)*np.cos(theta)
        M33 = (self.m1*self.ell1**2+self.m2*self.ell2**2+\
               self.J2z+self.J1y*np.sin(phi)**2+\
                self.J1z*np.cos(phi)**2)*np.cos(theta)**2\
                    +(self.J1x+self.J2x)*np.sin(theta)**2\
                        +self.m3*(self.ell3x**2+self.ell3y**2)+self.J3z
        N33 = 2*(self.J1x+self.J2x-self.m1*self.ell1**2-self.m2*self.ell2**2-self.J2z\
                 -self.J1y*np.sin(phi)**2-self.J1z*np.cos(phi)**2)*np.sin(theta)*np.cos(theta)
        M = np.array([[self.J1x, 0, -self.J1x*np.sin(theta)],
                      [0, M22, M23],
                      [-self.J1x*np.sin(theta), M23, M33]
                      ])
        C = np.array([[(self.J1y-self.J1z)*np.sin(phi)*np.cos(phi)*\
                       (thetadot**2-np.cos(theta)**2*psidot**2)\
                       +((self.J1y-self.J1z)*(np.cos(phi)**2-np.sin(phi)**2)-self.J1x)\
                        *np.cos(theta)*thetadot*psidot],
                      [2*(self.J1z-self.J1y)*np.sin(phi)*np.cos(phi)*phidot*thetadot+\
                       ((self.J1y-self.J1z)*(np.cos(phi)**2-np.sin(phi)**2)+self.J1x)\
                        *np.cos(theta)*phidot*psidot-0.5*N33*psidot**2],
                      [thetadot**2*(self.J1z-self.J1y)*np.sin(phi)*np.cos(phi)*np.sin(theta)\
                        +((self.J1y-self.J1z)*(np.cos(phi)**2-np.sin(phi)**2)\
                          -self.J1x)*np.cos(theta)*phidot*thetadot\
                            +(self.J1z-self.J1y)*np.sin(phi)*np.cos(phi)*np.sin(theta)*thetadot**2\
                                +2*(self.J1y-self.J1z)*np.sin(phi)*np.cos(phi)*phidot*psidot\
                                    +2*(-self.m1*self.ell1**2-self.m2*self.ell2**2-self.J2z\
                                        +self.J1x\
                                            +self.J2x+\
                                                self.J1y*np.sin(phi)**2\
                                                    +self.J1z*np.sin(phi)**2)*np.sin(theta)\
                                                        *np.cos(theta)*thetadot*psidot],
                     ])
        partialP = np.array([[0],
                             [(self.m1*self.ell1+self.m2*self.ell2)*P.g*np.cos(theta)],
                             [0],
                            ])
        force = P.km * (pwm_left + pwm_right) 
        torque = self.d * P.km * (pwm_left - pwm_right)
        tau = np.array([[torque],
                        [self.ellT*force*np.cos(phi)],
                        [self.ellT*force*np.cos(theta)*np.sin(phi)-torque*np.sin(theta)]])
        B = 0.001*np.array([[1,0,0],
                        [0,1,0],
                        [0,0,1]])
        qddot = np.linalg.inv(M) @ (-C - partialP + tau - B @ state[3:6])
        phiddot = qddot[0][0]
        thetaddot = qddot[1][0]
        psiddot = qddot[2][0]
        # build xdot and return
        xdot = np.array([[phidot],
                         [thetadot],
                         [psidot],
                         [phiddot],
                         [thetaddot],
                         [psiddot]])
        return xdot

    def h(self):
        # return y = h(x)
        phi = self.state[0][0]
        theta = self.state[1][0]
        psi = self.state[2][0]
        y = np.array([[phi], [theta], [psi]])
        return y

    def rk4_step(self, u):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + P.Ts / 2 * F1, u)
        F3 = self.f(self.state + P.Ts / 2 * F2, u)
        F4 = self.f(self.state + P.Ts * F3, u)
        self.state += P.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)


def saturate(u, limit):
    for i in range(0, u.shape[0]):
        if abs(u[i][0]) > limit:
            u[i][0] = limit * np.sign(u[i][0])
    return u
