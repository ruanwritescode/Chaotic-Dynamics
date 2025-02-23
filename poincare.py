import numpy as np
import matplotlib.pyplot as plt

def simple_poincare_section(trajectory, times, T):
    # Find points where trajectory crosses section
    section_points = []
    
    for i in range(len(times)-1):
        if times[i] % T <= times[i+1] % T:  # Crossing detected
            section_points.append(trajectory[i])
    
    return np.array(section_points)

def generate_pendulum_trajectory(theta0, omega0, tmax, dt):
    # Simple pendulum simulation
    t = np.arange(0, tmax, dt)
    theta = [theta0]
    omega = [omega0]
    
    for i in range(1, len(t)):
        omega.append(omega[-1] - np.sin(theta[-1]) * dt)
        theta.append(theta[-1] + omega[-1] * dt)
    
    return np.array([theta, omega]).T, t

def interpolated_poincare_section(trajectory, times, T):
    section_points = []
    
    for i in range(len(times)-1):
        t1, t2 = times[i], times[i+1]
        if t1 % T <= t2 % T:
            # Linear interpolation
            alpha = (T - t1 % T) / (t2 % T - t1 % T)
            point = trajectory[i] + alpha * (trajectory[i+1] - trajectory[i])
            section_points.append(point)
    
    return np.array(section_points)

def lorenz_spatial_section(trajectory, condition_func):
    section_points = []
    
    for i in range(len(trajectory)-1):
        p1, p2 = trajectory[i], trajectory[i+1]
        if condition_func(p1) * condition_func(p2) <= 0:  # Crossing detected
            # Linear interpolation
            alpha = abs(condition_func(p1)) / (abs(condition_func(p1)) + abs(condition_func(p2)))
            point = p1 + alpha * (p2 - p1)
            section_points.append(point)
    
    return np.array(section_points)

# Example condition functions
def y_equals_20(point):
    return point[1] - 20

def y_equals_2x(point):
    return point[1] - 2*point[0]

