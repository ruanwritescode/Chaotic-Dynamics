import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox

# Define the pendulum function
def pendfunc(state, t, args):
    B = args["B"]
    A = args["A"]
    alpha = args["alpha"]
    theta, omega = state
    m = 0.1  # kg
    l = 0.1  # m
    g = 9.8  # Gravity
    
    dtheta = omega
    domega = (A * np.cos(alpha * t) - m * g * np.sin(theta) - B * l * omega) / (m * l)
    
    return np.array([dtheta, domega])

# RK4 solver
def rk4(t0, h, n, xn, func, args):
    state_vectors = np.array([xn])
    t = t0

    for _ in range(n):
        k1 = h * func(xn, t, args)
        k2 = h * func(xn + k1 / 2, t + h / 2, args)
        k3 = h * func(xn + k2 / 2, t + h / 2, args)
        k4 = h * func(xn + k3, t + h, args)

        xn += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        state_vectors = np.append(state_vectors, [xn], axis=0)
        t += h

    return state_vectors

# Initial parameters
h = 0.005
n_steps = 1000
t0 = 0
init_theta = 3.0
init_omega = 0.1
B = 0.0
A = 0.0
alpha = 0.0
ymin, ymax = -20, 20  # Default plot bounds

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 5))
plt.subplots_adjust(left=0.1, bottom=0.45)

# Compute initial solution
xn = np.array([init_theta, init_omega])
args = {"B":B,"A":A,"alpha":alpha}
data = rk4(t0, h, n_steps, xn, pendfunc, args)

# Extract results
theta_vals = data[:, 0]
omega_vals = data[:, 1]
time_vals = np.linspace(t0, t0 + n_steps * h, n_steps + 1)

# Plot initial data
theta_line, = ax.plot(time_vals, theta_vals, label="θ")
omega_line, = ax.plot(time_vals, omega_vals, label="ω")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Values")
ax.set_title("Runge-Kutta 4th Order - Simple Pendulum")
ax.set_ylim(ymin, ymax)  # Set initial y-axis bounds
ax.legend()
ax.grid()

# Add sliders
ax_theta = plt.axes([0.1, 0.3, 0.3, 0.03])
ax_omega = plt.axes([0.1, 0.25, 0.3, 0.03])
ax_B = plt.axes([0.1, 0.2, 0.3, 0.03])
ax_A = plt.axes([0.6, 0.3, 0.3, 0.03])
ax_alpha = plt.axes([0.6, 0.25, 0.3, 0.03])
ax_h = plt.axes([0.6, 0.2, 0.3, 0.03])

s_theta = Slider(ax_theta, "θ₀", -np.pi, np.pi, valinit=init_theta, valstep=.01)
s_omega = Slider(ax_omega, "ω₀", -2, 2, valinit=init_omega)
s_B = Slider(ax_B, "B", 0, 2, valinit=B)
s_A = Slider(ax_A, "A", 0, 2, valinit=A)
s_alpha = Slider(ax_alpha, "α", 0, 10, valinit=alpha)
s_h = Slider(ax_h, "Timestep (h)", 0.001, 0.02, valinit=h, valstep=0.001)

# Add input boxes for y-axis bounds
ax_text_ymin = plt.axes([0.1, 0.05, 0.08, 0.03])
ax_text_ymax = plt.axes([0.25, 0.05, 0.08, 0.03])

t_ymin = TextBox(ax_text_ymin, "ymin", initial=str(ymin))
t_ymax = TextBox(ax_text_ymax, "ymax", initial=str(ymax))

# Update function
def update(val):
    new_theta = s_theta.val
    new_omega = s_omega.val
    new_B = s_B.val
    new_A = s_A.val
    new_alpha = s_alpha.val
    new_h = s_h.val

    # Update number of steps to maintain total simulation time
    new_n_steps = int(5 / new_h)  # Keeping total simulation time ~5s

    # Solve ODE with updated values
    xn = np.array([new_theta, new_omega])
    args = {"B": new_B, "A":new_A, "alpha":new_alpha}
    data = rk4(t0, new_h, new_n_steps, xn, pendfunc, args)
    
    theta_vals = data[:, 0]
    omega_vals = data[:, 1]
    time_vals = np.linspace(t0, t0 + new_n_steps * new_h, new_n_steps + 1)

    # Update plots
    theta_line.set_xdata(time_vals)
    omega_line.set_xdata(time_vals)
    theta_line.set_ydata(theta_vals)
    omega_line.set_ydata(omega_vals)

    ax.set_xlim(t0, t0 + new_n_steps * new_h)  # Adjust x-axis
    fig.canvas.draw_idle()

# Update function for y-axis bounds
def update_ybounds(value):
    try:
        ymin = float(t_ymin.text)
        ymax = float(t_ymax.text)
        ax.set_ylim(ymin, ymax)
        fig.canvas.draw_idle()
    except ValueError:
        pass  # Ignore invalid inputs

# Connect sliders to update function
s_theta.on_changed(update)
s_omega.on_changed(update)
s_B.on_changed(update)
s_A.on_changed(update)
s_alpha.on_changed(update)
s_h.on_changed(update)

# Connect text boxes to update function
t_ymin.on_submit(update_ybounds)
t_ymax.on_submit(update_ybounds)

plt.show()