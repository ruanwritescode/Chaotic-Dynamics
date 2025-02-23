import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def lorenz(xn, t, args):
    a, b, r = args["a"], args["b"], args["r"]
    x, y, z = xn
    dx = a * (y - x)
    dy = r * x - y - x * z
    dz = x * y - b * z
    return np.array([dx, dy, dz])

def rk4_step(x, t, h, f, args):
    k1 = h * f(x, t, args)
    k2 = h * f(x + 0.5 * k1, t + 0.5 * h, args)
    k3 = h * f(x + 0.5 * k2, t + 0.5 * h, args)
    k4 = h * f(x + k3, t + h, args)
    return x + (1.0/6.0) * (k1 + 2*k2 + 2*k3 + k4)

def rk4(tn, h0, t_end, xn, func, tol=0.001, args=None):
    state_vectors = np.array([xn])
    t = tn
    while t < t_end:
        h = h0
        error = float('inf')
        while error > tol:
            h = h / 2
            xplus = rk4_step(xn, t, h, func, args)
            x2 = rk4_step(xplus, t + h, h, func, args)
            xnext = rk4_step(xn, t, 2 * h, func, args)
            d1 = np.array(x2 - xnext)
            error = max(np.abs(d1))
        xn = xnext
        h = h * 2
        state_vectors = np.append(state_vectors, [xn], axis=0)
        t += h
    return state_vectors

def update(val):
    tol = slider.val
    lorenz_data = rk4(0, h_initial, t_end, lorenz_x0, lorenz, tol, lorenz_args)
    ax.clear()
    ax.plot(lorenz_data[:,0], lorenz_data[:,2], '.', markersize=4, label=f'Adaptive RK4, tol={tol:.4f}')
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_title('Lorenz Attractor')
    ax.legend()
    ax.grid(True)
    plt.draw()

lorenz_args = {"a": 16, "r": 45, "b": 4}
lorenz_x0 = [-13, -12, 52]
h_initial = .1
t_end = 20

fig, ax = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(bottom=0.15)

ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03])
slider = Slider(ax_slider, 'Tolerance', 0.0001, 0.5, valinit=0.01, valstep=0.0001)
slider.on_changed(update)

update(0.01)
plt.show()
