import numpy as np
import matplotlib.pyplot as plt

def lorenz(xn, t, args):
    a = args["a"]
    b = args["b"]
    r = args["r"]
    x, y, z = xn

    dx = a * (y - x)
    dy = r * x - y - x * z
    dz = x * y - b * z

    return np.array([dx, dy, dz])

def rossler(xn, t, args):
    a = args["a"]
    b = args["b"]
    c = args["c"]
    x, y, z = xn

    dx = -y-z
    dy = x + a * y
    dz = b + z*(x-c)

    return np.array([dx,dy,dz])

def rk4_step(x, t, h, f, args):
    """
    Performs one step of fourth-order Runge-Kutta method.
    """
    k1 = h * f(x, t, args)
    k2 = h * f(x + 0.5 * k1, t + 0.5 * h, args)
    k3 = h * f(x + 0.5 * k2, t + 0.5 * h, args)
    k4 = h * f(x + k3, t + h, args)
    return x + (1.0/6.0) * (k1 + 2*k2 + 2*k3 + k4)

# RK4 solver
def rk4(tn, h0, t_end, xn, func, args=None):
    state_vectors = np.array([xn])
    tol = 0.001
    t = tn

    while t < t_end:
        h = 2*h0
        error = float('inf')
        while error > tol:
            h = h/2
            if h < 1e-6:
                break
            xplus = rk4_step(xn, t, h, func, args)
            x2 = rk4_step(xplus, t + h, h, func, args)
            xn = rk4_step(xn, t, 2*h, func, args)
            d1 = x2 - xn
            error = np.linalg.norm(d1)
        # if(np.isnan(error)):
        #     break
        state_vectors = np.append(state_vectors, [xn], axis=0)
        t += h

    return state_vectors

lorenz_args = {"a":16,"r":45,"b":4}
lorenz_x0 = [-13,-12,52]
h_initial = .01
t_end = 20
lorenz_data = rk4(0, h_initial, t_end, lorenz_x0, lorenz, lorenz_args)

# plt.figure(figsize=(12, 10))
# plt.plot(lorenz_data[:,0], lorenz_data[:,2], '.', markersize=4, label='Adaptive RK4')
# plt.xlabel('x')
# plt.ylabel('z')
# plt.title('Lorenz Attractor (Adaptive RK4, r=45)')
# plt.legend()
# plt.grid(True)
# plt.show()

rossler_args = {"a":.2,"b":.2,"c":5.7}
rossler_x0 = [1,1,1]
t_end = 100
rossler_data = rk4(0, h_initial, t_end, rossler_x0, rossler, rossler_args)

print(rossler_data)

plt.figure(figsize=(12, 10)).add_subplot(projection='3d')
plt.plot(rossler_data[:,0], rossler_data[:,1], rossler_data[:,2], '.', markersize=4, label='Adaptive RK4')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Rossler (Adaptive RK4)')
plt.legend()
plt.grid(True)
plt.show()

# .add_subplot(projection='3d')