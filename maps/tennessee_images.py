#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:30:22 2023

@author: jayb

making the final image
"""
import geopandas as gpd
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology, filters


# read binary images. these are negative. 0 in riv means yes riv
ten = plt.imread('../images/layer_tn_state.png')[:, :, 0]
usa = plt.imread('../images/layer_tn_usa.png')[:, :, 0]
riv = plt.imread('../images/layer_tn_rivers.png')[:, :, 0]
lac = plt.imread('../images/layer_tn_lakes.png')[:, :, 0]

# binarize
thresh = 0.5
ten = ten < thresh
usa = usa < thresh
riv = riv < thresh
lac = lac < thresh

# get the sea
sea = ~ten & ~usa

# combime lakes, rivers, and sea into water
wat = lac | riv | sea

# want water, tn, and us as mutually-exclusive arrays
ten = ten & ~wat
usa = usa & ~wat

# trim to size, keep it symmetrical or the projection will be off (assuming square and proj centre in centre of img)
in_size = ten.shape[0]
trim = 5 # percent of image
trim = int(np.around((trim / 100) * in_size, 0))

new_a = trim
new_b = in_size - trim

ten = ten[new_a:new_b, new_a:new_b].copy()
usa = usa[new_a:new_b, new_a:new_b].copy()
wat = wat[new_a:new_b, new_a:new_b].copy()


# get coordinates of multilabelled pixels
total = ten * 1 + usa * 1 + wat * 1
coords_mult = np.argwhere(total > 1)

# reassign in the preferred order: water, region of interest, rest of world
for coord in coords_mult:
    if wat[coord[0], coord[1]]:
        ten[coord[0], coord[1]] = False
        usa[coord[0], coord[1]] = False
    elif ten[coord[0], coord[1]]:
        usa[coord[0], coord[1]] = False
    else:
        print('problem with multi fill')



# make sure no pixels are unlabelled or multiply labelled
total = ten * 1 + usa * 1 + wat * 1

assert (total == 0).sum() == 0
assert (total == 1).sum() == total.shape[0] * total.shape[1]
assert (total > 1).sum() == 0



# define colours for water, roi, and other land
c_wat = [100, 139, 190, 255]
c_ten = [195, 231, 198, 255]
c_usa = [240, 255, 240, 255]

img_wat = np.dstack([np.ones_like(wat) * wat] * 4) * c_wat
img_ten = np.dstack([np.ones_like(ten) * ten] * 4) * c_ten
img_usa = np.dstack([np.ones_like(usa) * usa] * 4) * c_usa

img_out = img_wat + img_ten + img_usa
assert img_out.max() <= 255
img_out = img_out / 255.0




plt.imsave(
    f'../images/maps/TN.png',
    img_out,
)

















