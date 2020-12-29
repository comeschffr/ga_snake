import numpy as np
import matplotlib.pyplot as plt
import random

plt.ion()
figure, ax = plt.subplots()
line, = ax.plot([],[], '-')

plt.axis(xmin=0, xmax=1, ymin=0, ymax=100)


def update_line(figure, line, new_x, new_y):
    new_xdata = np.append(line.get_xdata(), new_x)
    new_ydata = np.append(line.get_ydata(), new_y)

    line.set_xdata(new_xdata)
    line.set_ydata(new_ydata)
    
    plt.xlim([0, max(1, new_x)])
    if np.max(new_ydata) >= line.axes.get_ylim()[1]:
        plt.ylim([0, np.max(new_ydata)])

    figure.canvas.draw()
    figure.canvas.flush_events()

for i in range(100):
    update_line(figure, line, i, random.randrange(100))

plt.savefig('results_ga/final_plot.png')