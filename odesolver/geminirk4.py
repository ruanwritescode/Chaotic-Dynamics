import numpy
import matplotlib.pyplot as plt

# Lorenz system parameters
a_lorenz = 16.0
b_lorenz = 4.0

def lorenz_f(x, t, r=45.0):
    """
    Defines the Lorenz system ODEs.

    Args:
        x (numpy.ndarray): State vector [x, y, z].
        t (float): Current time (not used in Lorenz equations).
        r (float): Parameter r for the Lorenz system.

    Returns:
        numpy.ndarray: Derivative vector [dx/dt, dy/dt, dz/dt].
    """
    x_val, y_val, z_val = x
    dxdt = a_lorenz * (y_val - x_val)
    dydt = r * x_val - y_val - x_val * z_val
    dzdt = x_val * y_val - b_lorenz * z_val
    return numpy.array([dxdt, dydt, dzdt])

# Adaptive RK4 integrator from previous response (ensure it's the same)
def rk4_step(x, t, h, f):
    """
    Performs one step of fourth-order Runge-Kutta method.
    """
    k1 = h * f(x, t)
    k2 = h * f(x + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(x + 0.5 * k2, t + 0.5 * h)
    k4 = h * f(x + k3, t + h)
    return x + (1.0/6.0) * (k1 + 2*k2 + 2*k3 + k4)

def calculate_error(x_current, t_current, h, f):
    """
    Calculates error estimate by comparing one step of size 2h with two steps of size h.
    """
    x_half_step = rk4_step(x_current, t_current, h, f)
    x_h = rk4_step(x_half_step, t_current + h, h, f)
    x_2h = rk4_step(x_current, t_current, 2*h, f)
    delta = x_2h - x_h
    return x_h, x_2h, delta

def adaptive_rk4_integrator(x_initial, t_initial, t_end, h_initial, f, tolerance=0.001, h_min=1e-6):
    """
    Adaptive time-step fourth-order Runge-Kutta integrator.
    """
    current_x = numpy.array(x_initial)
    current_t = t_initial
    h = h_initial
    output_times = [current_t]
    output_states = [current_x]

    while current_t < t_end:
        if h < h_min:
            print("Warning: step size reached minimum value, exiting.")
            break

        x_h, x_2h, delta = calculate_error(current_x, current_t, h, f)
        error_norm = numpy.linalg.norm(delta, ord=numpy.inf)

        while error_norm > tolerance:
            h = h / 2
            if h < h_min:
                print("Warning: step size reached minimum value while reducing, exiting.")
                break
            x_h, x_2h, delta = calculate_error(current_x, current_t, h, f)
            error_norm = numpy.linalg.norm(delta, ord=numpy.inf)
        if h < h_min:
            break

        current_x = x_h
        current_t = current_t + 2*h
        output_times.append(current_t)
        output_states.append(current_x)
        # print(f"Time: {current_t:.4f}, State: {current_x}, Step size: {2*h:.4f}, Error: {error_norm:.4e}") # Reduced verbosity

    return output_times, output_states

# Non-adaptive RK4 integrator (from PS4, simplified)
def non_adaptive_rk4_integrator(x_initial, t_initial, t_end, h_fixed, f):
    """
    Non-adaptive fixed time-step fourth-order Runge-Kutta integrator.
    """
    current_x = numpy.array(x_initial)
    current_t = t_initial
    output_times = [current_t]
    output_states = [current_x]
    h = h_fixed

    while current_t < t_end:
        current_x = rk4_step(current_x, current_t, h, f)
        current_t += h
        output_times.append(current_t)
        output_states.append(current_x)
    return output_times, output_states


# (a) Plotting the Lorenz attractor with adaptive integrator
print("(a) Plotting Lorenz attractor with adaptive integrator...")
x0_lorenz = numpy.array([-13.0, -12.0, 52.0])
t0_lorenz = 0.0
t_end_lorenz = 20.0
h_initial_lorenz = 0.01

adaptive_times_lorenz, adaptive_states_lorenz = adaptive_rk4_integrator(
    x0_lorenz, t0_lorenz, t_end_lorenz, h_initial_lorenz, lambda x, t: lorenz_f(x, t, r=45.0)
)

adaptive_x = [state[0] for state in adaptive_states_lorenz]
adaptive_z = [state[2] for state in adaptive_states_lorenz]

plt.figure(figsize=(8, 6))
plt.plot(adaptive_x, adaptive_z, '.', markersize=4, label='Adaptive RK4')
plt.xlabel('x')
plt.ylabel('z')
plt.title('Lorenz Attractor (Adaptive RK4, r=45)')
plt.legend()
plt.grid(True)
plt.show()


# (b) Comparing adaptive and non-adaptive integrators
print("(b) Comparing adaptive and non-adaptive integrators...")
h_fixed_lorenz = 0.001
non_adaptive_times_lorenz, non_adaptive_states_lorenz = non_adaptive_rk4_integrator(
    x0_lorenz, t0_lorenz, t_end_lorenz, h_fixed_lorenz, lambda x, t: lorenz_f(x, t, r=45.0)
)

non_adaptive_x = [state[0] for state in non_adaptive_states_lorenz]
non_adaptive_z = [state[2] for state in non_adaptive_states_lorenz]

# Plotting a short segment for comparison
segment_length = 5.0 # Time units
segment_adaptive_indices = [i for i, t in enumerate(adaptive_times_lorenz) if t <= segment_length]
segment_non_adaptive_indices = [i for i, t in enumerate(non_adaptive_times_lorenz) if t <= segment_length]

plt.figure(figsize=(8, 6))
plt.plot([adaptive_states_lorenz[i][0] for i in segment_adaptive_indices], [adaptive_states_lorenz[i][2] for i in segment_adaptive_indices], 'r.', markersize=4, label='Adaptive RK4 (Segment)')
plt.plot([non_adaptive_states_lorenz[i][0] for i in segment_non_adaptive_indices], [non_adaptive_states_lorenz[i][2] for i in segment_non_adaptive_indices], 'b.', markersize=1, label='Non-adaptive RK4 (Segment)')
plt.xlabel('x')
plt.ylabel('z')
plt.title('Lorenz Segment (Adaptive vs Non-adaptive)')
plt.legend()
plt.grid(True)
plt.show()

print("Are the two solutions (adaptive and non) agree?  For a short segment, they appear to agree, tracing similar paths initially, but small deviations can be expected to grow in chaotic systems over longer time scales.")
print("Are the points produced by the adaptive solver evenly spaced in time? No, the time steps in the adaptive solver are not evenly spaced, as can be observed by examining the `adaptive_times_lorenz` output (or by uncommenting the time step printing in `adaptive_rk4_integrator`).")


# (c) Exploring different 'r' values
print("(c) Exploring different 'r' values...")

r_values_c = [0.5, 13.6, 13.9, 25.0, 28.0]
initial_conditions_c = [x0_lorenz, numpy.array([1.0, 1.0, 1.0]), numpy.array([5.0, 5.0, 5.0]), numpy.array([-20.0, 10.0, 0.0])]

for r_val in r_values_c:
    print(f"\nExploring r = {r_val}:")
    for ic_idx, ic in enumerate(initial_conditions_c):
        adaptive_times_r, adaptive_states_r = adaptive_rk4_integrator(
            ic, t0_lorenz, t_end_lorenz, h_initial_lorenz, lambda x, t: lorenz_f(x, t, r=r_val)
        )
        adaptive_x_r = [state[0] for state in adaptive_states_r]
        adaptive_z_r = [state[2] for state in adaptive_states_r]

        plt.figure(figsize=(6, 4))
        plt.plot(adaptive_x_r, adaptive_z_r, 'o', markersize=2)
        plt.xlabel('x')
        plt.ylabel('z')
        plt.title(f'Lorenz System (Adaptive RK4, r={r_val}, IC={ic_idx+1})')
        plt.grid(True)
        plt.show()

        if r_val == 0.5:
            print("  r=0.5: For r < 1, the origin (0,0,0) is a stable fixed point. Trajectories spiral towards the origin regardless of initial conditions.")
        elif 13.5 <= r_val <= 14: # e.g., 13.6, 13.9
            print(f"  r={r_val}: For r slightly above 13.456..., we expect stable fixed points to emerge besides the origin. Depending on the initial conditions, the system might converge to one of these stable fixed points or exhibit more complex behaviors but not fully chaotic yet.  Perhaps limit cycles or transient chaos.")
        elif 23 <= r_val <= 30: # e.g., 25, 28
            print(f"  r={r_val}: For higher r values, the system enters the chaotic regime. We observe the strange attractor. Trajectories are bounded but non-periodic and sensitive to initial conditions. The 'butterfly' shape becomes apparent.")