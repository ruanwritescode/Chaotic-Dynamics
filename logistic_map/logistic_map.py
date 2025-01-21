import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np

r = 2.5
m = 10
k = 0
x0 = 0.2

disp = 0

x = np.empty(m)
x[0] = x0
xn = np.linspace(0,.999999,1000)
xnplus = np.empty(1000)
webx = []
weby = []

for n in range(len(xn)):
    xnplus[n] = min(r,4) * xn[n] * (1 - xn[n])

for n in range(m-1):
    x[n+1] = r * x[n] * (1 - x[n])
    webx.append(x[n])
    weby.append(x[n])
    webx.append(x[n])
    weby.append(x[n+1])

    

n = np.arange(k,m)

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.canvas.manager.set_window_title('Logistic Map')
ax1.plot(n,x[k:], label="x_n versus n", linestyle = 'none', marker='o', markerfacecolor = 'w')
ax2.plot([0,1],[0,1],label="xn to xn+1")
ax2.plot(xn, xnplus, label="curve")
ax2.plot(webx, weby, color = 'r', label='cobweb')
parameters = '\n R = ' + str(r) +  ' x\u2080 = ' + str(x0)
ax1.set_title("x\u2099 versus n" + parameters)
ax1.set_xlabel("n")
ax1.set_ylabel("x\u2099")
ax2.set_title("x\u2099\u208A\u2081 versus x\u2099" + parameters)
ax2.set_xlabel("x\u2099")
ax2.set_ylabel("x\u2099\u208A\u2081")
ax1.text(disp, x[disp], '(' + str(disp) + ', ' + str(x[disp]) +')')

plot1 = 0
plot2 = 0
num_plots1 = 3
num_plots2 = 2

def update_plot(xinit, Rnew, mfloat, kfloat, plot1change, plot2change, newDisp):
    global plot1
    global plot2
    global r
    global m
    global k
    global x0
    global x
    global xnplus
    global disp
    disp = max(k,min(int(newDisp),m-plot1-1))
    plot1 = plot1change
    plot2 = plot2change
    r = Rnew
    x0 = xinit
    m = round(int(mfloat))
    k = round(int(kfloat))

    x = np.empty(m)
    x[0] = x0
    xn = np.linspace(0,.999999,1000)
    webx = []
    weby = []
    for n in range(len(xn)):
        xnplus[n] = min(r,4) * xn[n] * (1 - xn[n])
    if(plot2):
        for n in range(len(xn)):
            xnplus[n] = min(r,4) * xnplus[n] * (1 - xnplus[n])

    for n in range(m-1):
        x[n+1] = r * x[n] * (1 - x[n])
    n = 0
    while n < m-2:
        webx.append(x[n])
        weby.append(x[n])
        webx.append(x[n])
        weby.append(x[n+1+plot2])
        n = n + plot2 + 1

    n = np.arange(k,m)
    ax1.clear()
    parameters = '\n R = ' + str(r) +  ' x\u2080 = ' + str(x0)
    if(plot1 == 0):
        ax1.plot(n,x[k:], linestyle = 'none', marker='o', markerfacecolor = 'w')
        ax1.set_title("x\u2099 versus n" + parameters)
        ax1.set_xlabel("n")
        ax1.set_ylabel("x\u2099")
        ax1.text(disp, x[disp], '(' + str(disp) + ', ' + str(round(x[disp],3)) +')')
    elif(plot1 == 1):
        ax1.plot(x[k:-plot1],x[k+plot1:], linestyle = 'none', marker='.')
        ax1.set_title("x\u2099\u208A\u2081 versus x\u2099" + parameters)
        ax1.set_xlabel("x\u2099")
        ax1.set_ylabel("x\u2099\u208A\u2081")
        ax1.text(x[disp], x[disp+plot1], '(' + str(x[disp]) + ', ' + str(round(x[disp+plot1],3)) +')')
    elif(plot1 == 2):
        ax1.plot(x[k:-plot1],x[k+plot1:], linestyle = 'none', marker='.')
        ax1.set_title("x\u2099\u208A\u2082 versus x\u2099" + parameters)
        ax1.set_xlabel("x\u2099")
        ax1.set_ylabel("x\u2099\u208A\u2082")
        ax1.text(x[disp], x[disp+plot1], '(' + str(x[disp]) + ', ' + str(round(x[disp+plot1],3)) +')')

    ax2.clear()
    ax2.plot([0,1],[0,1],label="xn to xn+2")
    ax2.plot(xn, xnplus, label="curve")
    ax2.plot(webx[k:], weby[k:], color = 'r', label='cobweb')
    ax2.set_xlabel("x\u2099")
    if(plot2 == 0):
        ax2.set_title("x\u2099\u208A\u2081 versus x\u2099" + parameters)
        ax2.set_ylabel("x\u2099\u208A\u2081")
    elif(plot2 == 1):
        ax2.set_title("x\u2099\u208A\u2082 versus x\u2099" + parameters)
        ax2.set_ylabel("x\u2099\u208A\u2082")

    global xinit_slider
    xinit_slider.valinit = xinit
    xinit_slider.reset()
    global R_slider
    R_slider.valinit = r
    R_slider.reset()
    global xinit_box
    xinit_box.set_val('')
    global R_box
    R_box.set_val('')
    fig.canvas.draw_idle()

plt.subplots_adjust(bottom=0.5)  # Make room for sliders

slider_x = .18
text_x = .92
ax1_button = plt.axes([slider_x, 0.34, 0.32, 0.03])
ax2_button = plt.axes([slider_x + .34, 0.34, 0.32, 0.03])

axnext_disp = plt.axes([slider_x + .34, 0.385, 0.15, 0.03])
axprev_disp = plt.axes([slider_x + .17, 0.385, 0.15, 0.03])

ax_xinit = plt.axes([slider_x, 0.28, 0.65, 0.03])
axbox_xinit = plt.axes([text_x, 0.28, 0.05, 0.03])
ax_R = plt.axes([slider_x, 0.2, 0.65, 0.03])
axbox_R = plt.axes([text_x, 0.2, 0.05, 0.03])
ax_m = plt.axes([slider_x, 0.12, 0.65, 0.03])
ax_k = plt.axes([slider_x, 0.04, 0.65, 0.03])

button1 = Button(ax1_button, 'Change Left Plot')
button2 = Button(ax2_button, 'Change Right Plot')
nextButton = Button(axnext_disp, 'Next x',)
prevButton = Button(axprev_disp, 'Previous x',)

xinit_slider = plt.Slider(ax_xinit, 'x\u2080', 0.0, 1.1, valinit=x0,valstep=0.01)
xinit_box = TextBox(axbox_xinit, '')
R_slider = plt.Slider(ax_R, 'R', 0, 4.5, valinit=r,valstep = 0.01)
R_box = TextBox(axbox_R, '')
m_slider = plt.Slider(ax_m, 'm',1,1000,valinit=m,valstep = 1)
k_slider = plt.Slider(ax_k, 'k (transient)',0,100,valinit=k,valstep=1)


button1.on_clicked(lambda val: update_plot(xinit_slider.val, R_slider.val, m_slider.val, k_slider.val, (plot1+1)%num_plots1, plot2, disp))
button2.on_clicked(lambda val: update_plot(xinit_slider.val, R_slider.val, m_slider.val, k_slider.val, plot1, (plot2+1)%num_plots2, disp))

nextButton.on_clicked(lambda val: update_plot(xinit_slider.val, R_slider.val, m_slider.val, k_slider.val, plot1, plot2, disp + 1))
prevButton.on_clicked(lambda val: update_plot(xinit_slider.val, R_slider.val, m_slider.val, k_slider.val, plot1, plot2, disp - 1))

xinit_slider.on_changed(lambda val: update_plot(val, R_slider.val, m_slider.val, k_slider.val, plot1, plot2, disp))
xinit_box.on_submit(lambda val: update_plot(float(val), R_slider.val, m_slider.val, k_slider.val, plot1, plot2, disp))

R_slider.on_changed(lambda val: update_plot(xinit_slider.val, val, m_slider.val, k_slider.val, plot1, plot2, disp))
R_box.on_submit(lambda val: update_plot(xinit_slider.val, float(val), m_slider.val, k_slider.val, plot1, plot2, disp))

m_slider.on_changed(lambda val: update_plot(xinit_slider.val, R_slider.val, val, k_slider.val, plot1, plot2, disp))
k_slider.on_changed(lambda val: update_plot(xinit_slider.val, R_slider.val, m_slider.val, val, plot1, plot2, disp))

plt.show()
