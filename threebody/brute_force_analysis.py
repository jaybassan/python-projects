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






# plot a histogram of the steps
hist = True
if hist:
    fig, ax = plt.subplots(figsize=(10,10))

    ax.hist(df['steps'], bins=128)

    plt.tight_layout()
    plt.show()


# visualise the lowest loss trajectory
best = df[df['steps'] == df['steps'].max()]

# unpack the values
I1, I2, I3 = df_to_input(best)

# get the trajectory
p1, p2, p3 = get_trajectories(I1, I2, I3)



fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(projection='3d')
plt.gca().patch.set_facecolor('black')

plt.plot([i[0] for i in p1], [j[1] for j in p1], [k[2] for k in p1] , '^', color='r', markersize = 1.0, alpha=0.5)
plt.plot([i[0] for i in p2], [j[1] for j in p2], [k[2] for k in p2] , '^', color='w', markersize = 1.0, alpha=0.5)
plt.plot([i[0] for i in p3], [j[1] for j in p3], [k[2] for k in p3] , '^', color='b', markersize = 1.0, alpha=0.5)

plt.axis('on')

window=100
ax.set_xlim(-window, window)
ax.set_ylim(-window, window)
ax.set_zlim(-window, window)

# # optional: use if reference axes skeleton is desired,
# # ie plt.axis is set to 'on'
# # ax.set_xticks([]), ax.set_yticks([]), ax.set_zticks([])

# # make pane's have the same colors as background
ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0)), ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0)), ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))

# # ax.view_init(elev = 20, azim = t)
# # plt.savefig('{}'.format(t), dpi=300, bbox_inches='tight')
plt.show()
# plt.close()





pass


