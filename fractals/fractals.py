import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def angleMat(angle):
    radians = angle * np.pi/180
    return np.array([[np.cos(radians), -np.sin(radians)], [np.sin(radians), np.cos(radians)]])

max_segments = 12
left_reduction = 0.6
right_reduction = 0.6

left_angle = 0
left_angle_mat = angleMat(left_angle)
right_angle = 0
right_angle_mat = angleMat(right_angle)

def branch(point, length, direction, depth):
    global segments
    global max_segments
    global left_reduction
    global right_reduction
    global left_angle
    global right_angle
    global left_angle_mat
    global right_angle_mat

    depth += 1

    if(left_reduction < 0):
        right_length = length*np.random.rand()
        left_length = length*np.random.rand()
    else:
        right_length = length*right_reduction
        left_length = length*left_reduction
    if(left_angle < 0):
        left_angle_mat = angleMat(np.random.randint(0,180))
        right_angle_mat = left_angle_mat

    

    right_vect = None
    left_vect = None
    right_direction = None
    left_direction = None


    if(length < 0.000001 or depth > max_segments):
        return
    if(direction == "up"):
        right_vect = np.dot(right_angle_mat, np.array([right_length, 0]))
        left_vect = np.dot(left_angle_mat, np.array([-left_length, 0]))
        right_direction = "right"
        left_direction = "left"
    elif(direction == "down"):
        right_vect = np.dot(right_angle_mat, np.array([-right_length, 0]))
        left_vect = np.dot(left_angle_mat, np.array([left_length, 0]))
        right_direction = "left"
        left_direction = "right"
    elif(direction == "right"):
        right_vect = np.dot(right_angle_mat, np.array([0, -right_length]))
        left_vect = np.dot(left_angle_mat, np.array([0, left_length]))
        right_direction = "down"
        left_direction = "up"
    elif(direction == "left"):
        right_vect = np.dot(right_angle_mat, np.array([0, right_length]))
        left_vect = np.dot(left_angle_mat, np.array([0, -left_length])) 
        right_direction = "up"
        left_direction = "down"
    right_point = np.add(point, right_vect)
    left_point = np.add(point, left_vect)
    segments = np.append(segments, [np.array([point,right_point]),np.array([point,left_point])], axis=0)
    branch(right_point, right_length, left_direction, depth)
    branch(left_point, left_length, right_direction, depth)

def update_plot(new_left_reduction = left_reduction, new_right_reduction=right_reduction, new_left_angle=left_angle, new_right_angle=right_angle):
    global segments
    global right_reduction
    global left_reduction
    global left_angle
    global right_angle
    global left_angle_mat
    global right_angle_mat

    right_reduction = new_right_reduction
    left_reduction = new_left_reduction
    left_angle = new_left_angle
    right_angle = new_right_angle

    left_angle_mat = angleMat(new_left_angle)
    right_angle_mat = angleMat(new_right_angle)

    segments = np.array([np.array([[0, 0],[0,1]])])

    branch([0,1], 1, "up", 0)
    ax.clear()
    lc = LineCollection(segments)
    ax.add_collection(lc)
    ax.autoscale()
    fig.canvas.draw_idle()

fig, ax = plt.subplots()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Plot of Fractal in 2D Cartesian Space")

plt.subplots_adjust(bottom=0.32)  # Make room for sliders

ax_right_reduction = plt.axes([0.18, 0.07, 0.65, 0.03])
right_reduction_slider = plt.Slider(ax_right_reduction, 'right_reduction', 0, 1.0, valinit=right_reduction,valstep=0.01)

ax_left_reduction = plt.axes([0.18, 0.12, 0.65, 0.03])
left_reduction_slider = plt.Slider(ax_left_reduction, 'left_reduction', -.01, 1.0, valinit=left_reduction,valstep=0.01)

ax_right_angle = plt.axes([0.18, 0.17, 0.65, 0.03])
right_angle_slider = plt.Slider(ax_right_angle, 'right_angle', 0, 360, valinit=right_angle,valstep=1)

ax_left_angle = plt.axes([0.18, 0.22, 0.65, 0.03])
left_angle_slider = plt.Slider(ax_left_angle, 'left_angle', -1, 360, valinit=left_angle,valstep=1)

update_plot(left_reduction, right_reduction, left_angle, right_angle)

left_reduction_slider.on_changed(lambda val: update_plot(val))
right_reduction_slider.on_changed(lambda val: update_plot(left_reduction, val))
left_angle_slider.on_changed(lambda val: update_plot(left_reduction, right_reduction, val, val))
right_angle_slider.on_changed(lambda val: update_plot(left_reduction, right_reduction, left_angle, val))

plt.show()

        