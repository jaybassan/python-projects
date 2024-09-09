# takes the starting params of a three body problem and makes a nice image
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *

# list the files
in_dir = './trajectories/'
files = [f for f in os.listdir(in_dir) if '.csv' in f]

# load and concat the dataframes
df = pd.concat([pd.read_csv(in_dir + f) for f in files])

# get the params wanted
params = df[df['steps'] == df['steps'].max()]

# unpack the values
I1, I2, I3 = df_to_input(params)

# get the trajectory
t1, t2, t3 = get_trajectories(I1, I2, I3)

# show it 
show = False
if show:
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(projection='3d')
    plt.gca().patch.set_facecolor('black')

    plt.plot([i[0] for i in t1], [j[1] for j in t1], [k[2] for k in t1] , '^', color='r', markersize = 1.0, alpha=0.5)
    plt.plot([i[0] for i in t2], [j[1] for j in t2], [k[2] for k in t2] , '^', color='w', markersize = 1.0, alpha=0.5)
    plt.plot([i[0] for i in t3], [j[1] for j in t3], [k[2] for k in t3] , '^', color='b', markersize = 1.0, alpha=0.5)

    plt.axis('on')


    window=100
    ax.set_xlim(-window, window)
    ax.set_ylim(-window, window)
    ax.set_zlim(-window, window)
    plt.show()
    plt.close()

# TODO
# gonna make a 2d image, so want to decide what dimension to squash and represent by colour, alpha etc
# want to figure out from which angle the trajectories have the best depth, as this is the best line 
# along which to compress to 2D for visualisation

# choose which dimension to collapse and represent with alpha or colour
# 0 = x, 1 = y, 2 = z
squash = 0

# normalize that dimension between 0 and 1
squash_min = np.min([t1[:, squash].min(), t2[:, squash].min(), t3[:, squash].min()])
squash_max = np.max([t1[:, squash].max(), t2[:, squash].max(), t3[:, squash].max()])
squash_max -= squash_min

t1[:, squash] -= squash_min
t2[:, squash] -= squash_min
t3[:, squash] -= squash_min

t1[:, squash] /= squash_max
t2[:, squash] /= squash_max
t3[:, squash] /= squash_max

# double check normalized
assert np.min([t1[:, squash].min(), t2[:, squash].min(), t3[:, squash].min()]) == 0.0
assert np.max([t1[:, squash].max(), t2[:, squash].max(), t3[:, squash].max()]) == 1.0

# translate the other two dimensions so no negative numbers
y_min = np.min([t1[:, 1].min(), t2[:, 1].min(), t3[:, 1].min()])
y_max = np.max([t1[:, 1].max(), t2[:, 1].max(), t3[:, 1].max()])

z_min = np.min([t1[:, 2].min(), t2[:, 2].min(), t3[:, 2].min()])
z_max = np.max([t1[:, 2].max(), t2[:, 2].max(), t3[:, 2].max()])

t1[:, 1] -= y_min
t1[:, 2] -= z_min

t2[:, 1] -= y_min
t2[:, 2] -= z_min

t3[:, 1] -= y_min
t3[:, 2] -= z_min

# make the non squashed dimensions integers in their own array and keep the squashed dimensions for alphas
coords1 = np.around(t1[:, 1:], 0).copy().astype(int)
coords2 = np.around(t2[:, 1:], 0).copy().astype(int)
coords3 = np.around(t3[:, 1:], 0).copy().astype(int)

depth1 = t1[:, squash].copy()[:, np.newaxis]
depth2 = t2[:, squash].copy()[:, np.newaxis]
depth3 = t3[:, squash].copy()[:, np.newaxis]

# colour and alpha array
colour1 = [0.9, 0.1, 0.1]
colour1 = np.array([colour1] * depth1.shape[0])
colour1 = np.hstack([colour1, depth1])

colour2 = [0.1, 0.9, 0.1]
colour2 = np.array([colour2] * depth2.shape[0])
colour2 = np.hstack([colour2, depth2])

colour3 = [0.1, 0.1, 0.9]
colour3 = np.array([colour3] * depth3.shape[0])
colour3 = np.hstack([colour3, depth3])

# make the image array
img = np.zeros((2000, 2000, 4))

# colour in the planets
img[tuple(coords1.T)] = colour1
img[tuple(coords2.T)] = colour2
img[tuple(coords3.T)] = colour3


plt.imshow(img)
plt.show()
