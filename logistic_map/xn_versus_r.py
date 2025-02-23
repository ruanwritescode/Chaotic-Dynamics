import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np

m = 250
k = 150
x0 = 0.2
r_density = 100
r_low = 1
r_high = 3.9999
    
fig, ax1 = plt.subplots()
fig.canvas.manager.set_window_title('x\u2099 vs. r')



def logFunc():
    return None

def update_plot(xinit = x0, mfloat = m, kfloat = k, new_r_low=r_low, new_r_high=r_high):
    global m
    global k
    global x0
    global r_density
    global r_low
    global r_high

    x0 = xinit
    m = round(int(mfloat))
    k = round(int(kfloat))
    r_low = new_r_low
    r_high = new_r_high

    r_range = np.linspace(r_low,r_high,r_density)
    x = np.full((r_density, m-k), x0)

    for n in range(len(r_range)):
        for _ in range(k):
            x0 = r_range[n] * x0 * (1 - x0)
        x[0] = x0
        for i in range(1, m-k):
            x[n][i] = r_range[n] * x[n][i-1] * (1 - x[n][i-1])

    ax1.clear()
    parameters = '\nR Low = ' + str(r_low) +  ' and R High = ' + str(r_high)
    ax1.plot(r_range,x, linestyle = 'none', marker='.',ms = .1, mec='b')
    ax1.set_title("x\u2099 versus R" + parameters)
    ax1.set_ylabel("x\u2099")
    ax1.set_xlabel("R")   


    global xinit_slider
    global xinit_box
    xinit_slider.valinit = x0
    xinit_slider.reset()
    xinit_box.set_val('')

    global R_low_slider
    global R_high_slider

    R_low_slider.valinit = r_low
    R_low_slider.valstep = (1/(r_low**10)) * .01
    R_low_slider.reset()

    R_high_slider.valinit = r_high
    R_high_slider.valstep = (1/(r_high**10)) * .01
    R_high_slider.reset()

    fig.canvas.draw_idle()

plt.subplots_adjust(bottom=0.4)  # Make room for sliders

slider_x = .18
text_x = .92

ax_xinit = plt.axes([slider_x, 0.28, 0.65, 0.03])
axbox_xinit = plt.axes([text_x, 0.28, 0.05, 0.03])

ax_R_low = plt.axes([slider_x, 0.2, 0.65, 0.03])
ax_R_high = plt.axes([slider_x, 0.12, 0.65, 0.03])

ax_k = plt.axes([slider_x, 0.04, 0.65, 0.03])

xinit_slider = plt.Slider(ax_xinit, 'x\u2080', 0.0, 1.1, valinit=x0,valstep=0.01)
xinit_box = TextBox(axbox_xinit, '')

R_low_slider = plt.Slider(ax_R_low, 'R Low', 1, 3.9999, valinit=r_low,valstep = (1/(r_low**4)) * .01)
R_high_slider = plt.Slider(ax_R_high, 'R High',1,3.9999,valinit=r_high,valstep = (1/(r_high**4)) * .01)

k_slider = plt.Slider(ax_k, 'k (transient)',0,250,valinit=k,valstep=10)

update_plot(x0, m, k, r_low, r_high)

xinit_slider.on_changed(lambda val: update_plot(val))
xinit_box.on_submit(lambda val: update_plot(float(val)))

R_low_slider.on_changed(lambda val: update_plot(x0, m, k, val, r_high))
R_high_slider.on_changed(lambda val: update_plot(x0, m, k, r_low, val))

k_slider.on_changed(lambda val: update_plot(x0, m, val))

plt.show()
