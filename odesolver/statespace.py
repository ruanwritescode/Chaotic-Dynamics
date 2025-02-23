import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the pendulum system
def pendfunc(state, t, B, A, alpha):
    theta, omega = state
    m, l, g = 0.1, 0.1, 9.8  # kg, m, gravity

    dtheta = omega
    domega = (A * np.cos(alpha * t) - m * g * np.sin(theta) - B * l * omega) / (m * l)

    return np.array([dtheta, domega])

# RK4 solver
def rk4(t0, h, n, xn, B, A, alpha):
    state_vectors = np.array([xn])
    t = t0
    theta_limit = 20
    for _ in range(n):
        k1 = h * pendfunc(xn, t, B, A, alpha)
        k2 = h * pendfunc(xn + k1 / 2, t + h / 2, B, A, alpha)
        k3 = h * pendfunc(xn + k2 / 2, t + h / 2, B, A, alpha)
        k4 = h * pendfunc(xn + k3, t + h, B, A, alpha)

        xn += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        state_vectors = np.append(state_vectors, [xn], axis=0)

        if abs(xn[0]) > theta_limit:
            break

        t += h

    return state_vectors

# **Smartly chosen initial conditions**
initial_conditions = [
    (0.0, 2.0), (0.0, 8.0), 
    (0.0, 12.0), (0.0, 15.0), (0.0, 18.0), 
    (-5.0, 5.049 * np.pi), (5.0, -5.049 * np.pi),
    (-5.0, 35.0), (-5.0, 25.0),
    (5.0, -35.0), (5.0, -25.0)
]

# Initial values
h = 0.005
n_steps = 2000
t0 = 0
B = 0
A = 0
alpha = (3 / 4) * 9.9  # Start around 3/4 of the natural frequency

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, bottom=0.3)

# Function to update the plot dynamically
def update(val):
    ax.clear()
    
    # Read new values from sliders
    A = slider_A.val
    alpha = slider_alpha.val
    B = slider_B.val
    h = slider_h.val

    # Generate state-space portrait
    for theta0, omega0 in initial_conditions:
        xn = np.array([theta0, omega0])
        data = rk4(t0, h, n_steps, xn, B, A, alpha)

        theta_vals = np.mod(data[:, 0] + np.pi, 2 * np.pi) - np.pi
        omega_vals = data[:, 1]

        ax.plot(theta_vals, omega_vals, marker='.', markersize=4, linestyle='none')

    # Labels and grid
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel(r'$\omega$')
    ax.set_title(f'State-Space Portrait (B={B}, A={A}, h={h}) Modulo 2π')
    ax.grid()
    
    fig.canvas.draw_idle()

# **Sliders**
ax_A = plt.axes([0.15, 0.15, 0.65, 0.03])  # (left, bottom, width, height)
ax_alpha = plt.axes([0.15, 0.1, 0.65, 0.03])
ax_B = plt.axes([0.15, 0.05, 0.65, 0.03])
ax_h = plt.axes([0.15, 0.2, 0.65, 0.03])

slider_A = Slider(ax_A, 'A', 0, 2.0, valinit=A, valstep=0.05)
slider_alpha = Slider(ax_alpha, r'$\alpha$', 0, 15.0, valinit=alpha, valstep=0.1)
slider_B = Slider(ax_B, 'B', 0, 1.0, valinit=B, valstep=0.01)
slider_h = Slider(ax_h, 'h', 0.001, 2, valinit=h, valstep=0.001)

# Update plot when sliders change
slider_A.on_changed(update)
slider_alpha.on_changed(update)
slider_B.on_changed(update)
slider_h.on_changed(update)

# Initial plot
update(0)

plt.show()