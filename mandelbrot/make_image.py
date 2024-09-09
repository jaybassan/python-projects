import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter



# load the array
resolution='16384'
array_in = np.load(f'./data/{resolution}x{resolution}-1024iterations.npy')

# cap to a certain iteration
cap = 512
img = np.clip(array_in, a_min=0, a_max=cap)

# process
# fill in numbers actually in the set with the minimum value for effect
img[img == img.max()] = img.min()

# root to emphasize lower values 
exp = 0.5
img = img ** exp



cmap = 'bone'

# fig, ax = plt.subplots(figsize=(20,20))


# ax.imshow(img, cmap=cmap)

# plt.tight_layout()
# plt.show()

plt.imsave(f'./imgs/resolution{resolution}-cap{cap}-{cmap}.png', img, dpi=300, cmap=cmap)
