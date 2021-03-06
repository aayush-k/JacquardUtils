import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import sys

fig = plt.figure()
csv_data = genfromtxt('./data/converted/{0}'.format(sys.argv[1]), delimiter=',')

# data = csv_data[1:, 2:17]
data = csv_data

# data is a n x 15 array
rows, cols = data.shape
data = np.hstack((data, np.zeros((data.shape[0], 1))))

vis_rows = cols * 3
vis_data = np.random.rand(vis_rows, cols)

im = plt.imshow(vis_data, animated=True)
i = 0

ani = None
pause = False

print("Often times the VERY first row of data is the beginning of the gesture you're trying to recognize.\nIn that case, would you like to start annotating with 1's? (y/n)")
annotate = (input().lower() == 'y')

# allows you to pause/play by clicking on figure
def onClickCanvas(event):
    global pause
    pause ^= True

    if pause:
        ani.event_source.stop()
    else:
        ani.event_source.start()

def onClickToggleAnnotate(event):
    global annotate
    annotate = not annotate
    plt.title("Positive Annotation" if annotate else "Negative Annotation")


# animation update function
def updatefig(*args):
    global vis_data, data, i, vis_rows, im, rows, ani, annotate
    try:
        vis_data[:,:] = data[i:i + vis_rows, :-1] # last column is y labels
    except:
        np.savetxt('./data/annotated/{0}'.format(sys.argv[1]), data, delimiter=',')
        print('Annotated file saved at ./data/annotated/{0}'.format(sys.argv[1]))
        plt.close(fig)
        sys.exit()

    if annotate:
        data[i,-1] = 1
    im.set_array(vis_data)
    i += 1
    return im,

plt.title("Positive Annotation" if annotate else "Negative Annotation")
fig.canvas.mpl_connect('button_press_event', onClickToggleAnnotate)
ani = animation.FuncAnimation(fig, updatefig, interval=10, blit=True)
plt.show()
