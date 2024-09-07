from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation
from IPython.display import HTML

n =800

r= np.linspace(0, 1, n)
theta = np.linspace(0, 2 * np.pi, n)

[R, THETA] = np.meshgrid(r, theta, indexing='ij')

petalNum = 5

tmp = petalNum * THETA
x = 1 - (1/2)*((5/4) * (1 - (tmp % (2 * np.pi)) / np.pi / 2) ** 2 - (1 / 4)) ** 2

phi = (np.pi / 2) * np.exp (-1/4)

y = 1.95653 * (R ** 2) * (1.27689 * R - 1) ** 2 * np.sin(phi)

R2 = x * (R * np.sin(phi) + y * np.cos(phi)) 

X = R2 * np.sin(THETA)
Y = R2 * np.cos(THETA)

Z = x * (R * np.cos(phi) - y * np.sin(phi))

mapSize = 20
blue_map = np.array([np.linspace(138,75, mapSize).T,
                    np.linspace(43,0, mapSize).T,
                    np.linspace(226,130, mapSize).T]).T

gold_map = np.array([[255,215,0], [250,210,0]])
violet_map = np.concatenate((gold_map, blue_map))

fig = plt.figure(figsize=(18,18))
ax = Axes3D(fig)
ax.set_facecolor('black')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.view_init(azim=12, elev=66)

newcmp = ListedColormap(violet_map / 255)
surf = ax.plot_surface(X,Y,Z,
                        cmap = newcmp,
                        linewidth = 0,
                        antialiased = False)

def animate(i):
    if i <= 180:
        elev = 15.6 + 0.28 * i
    else:
        elev = 66 - 0.28 * (i - 180)

    ax.view_init(elev=elev, azim=i)

    return fig,

anim = animation.FuncAnimation(fig,
                                animate,
                                frames = 360,
                                interval = 20,
                                blit = True)

anim.save('3D_purple_rosr.mp4', fps=30,
            extra_args=['-vcodec', 'libx264'])

HTML(anim.to_html5_video())




