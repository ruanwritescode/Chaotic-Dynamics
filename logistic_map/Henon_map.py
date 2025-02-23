import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np

m = 250
k = 150
x0 = 1.6
a_density = 500
a_low = 0
a_high = 1.4
    
fig, ax1 = plt.subplots()
fig.canvas.manager.set_window_title('x\u2099 vs. r')



def logFunc():
    return None

def update_plot(xinit = x0, mfloat = m, kfloat = k, new_a_low=a_low, new_a_high=a_high):
    global m
    global k
    global x0
    global a_density
    global a_low
    global a_high

    x0 = xinit
    m = round(int(mfloat))
    k = round(int(kfloat))
    a_low = new_a_low
    a_high = new_a_high
    b = 0.3

    a_range = np.linspace(a_low,a_high,a_density)
    x = np.full((a_density, m), x0)
    y = np.empty((a_density, m))

    for n in range(len(a_range)):
        for i in range(1, m):
            y[n][i] = b * x[n][i]
            x[n][i] = y[n][i] + 1 - a_range[n] * x[n][i-1]**2

    ax1.clear()
    parameters = '\na Low = ' + str(a_low) +  ' and a High = ' + str(a_high)
    ax1.plot(a_range,x[:, k:], linestyle = 'none', marker='.',ms = .1, mec='b')
    ax1.set_title("x\u2099 versus A" + parameters)
    ax1.set_ylabel("x\u2099")
    ax1.set_xlabel("A")   


    global xinit_slider
    global xinit_box
    xinit_slider.valinit = x0
    xinit_slider.reset()
    xinit_box.set_val('')

    global A_low_slider
    global A_high_slider

    A_low_slider.valinit = a_low
    A_low_slider.reset()

    A_high_slider.valinit = a_high
    A_high_slider.reset()

    fig.canvas.draw_idle()

plt.subplots_adjust(bottom=0.4)  # Make room for sliders

slider_x = .18
text_x = .92

ax_xinit = plt.axes([slider_x, 0.28, 0.65, 0.03])
axbox_xinit = plt.axes([text_x, 0.28, 0.05, 0.03])

ax_A_low = plt.axes([slider_x, 0.2, 0.65, 0.03])
ax_A_high = plt.axes([slider_x, 0.12, 0.65, 0.03])

ax_k = plt.axes([slider_x, 0.04, 0.65, 0.03])

xinit_slider = plt.Slider(ax_xinit, 'x\u2080', 0.0, 1.1, valinit=x0,valstep=0.01)
xinit_box = TextBox(axbox_xinit, '')

A_low_slider = plt.Slider(ax_A_low, 'A Low', 0, a_high, valinit=a_low,valstep =.01)
A_high_slider = plt.Slider(ax_A_high, 'A High',a_low,1.4,valinit=a_high,valstep = .01)

k_slider = plt.Slider(ax_k, 'k (transient)',0,250,valinit=k,valstep=10)

update_plot(x0, m, k, a_low, a_high)

xinit_slider.on_changed(lambda val: update_plot(val))
xinit_box.on_submit(lambda val: update_plot(float(val)))

A_low_slider.on_changed(lambda val: update_plot(x0, m, k, val, a_high))
A_high_slider.on_changed(lambda val: update_plot(x0, m, k, a_low, val))

k_slider.on_changed(lambda val: update_plot(x0, m, val))

plt.show()
