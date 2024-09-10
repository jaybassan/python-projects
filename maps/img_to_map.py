# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jay Bassan

Take processed shapefiles of lakes and rivers and save those of
a particular country, in a particular projection.
"""
import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology, filters

### parameters to change ###
country = 'Canada'

lake_size = '10sqkm'
river_size = '100cms'

dpi = 1800


cty = plt.imread(f'./images/{country}_{dpi}dpi.png')[:, :, 0]
riv = plt.imread(f'./images/rivers{river_size}_{dpi}dpi.png')[:, :, 0]
lac = plt.imread(f'./images/lakes{lake_size}_{dpi}dpi.png')[:, :, 0]
row = plt.imread(f'./images/non{country}_{dpi}dpi.png')[:, :, 0]

print('Loaded data.')

# binarize
thresh = 0.5
cty = cty < thresh
riv = riv < thresh
lac = lac < thresh
row = row < thresh


# get the sea
sea = ~cty & ~row

# combime lakes, rivers, and sea into water
wat = lac | riv | sea
wat = wat.copy()

del lac
del riv
del sea

#arrange so we have water, canada, and non canada as mutexcl arrays
cty = cty & ~wat
row = row & ~wat


# trim to required size, have to keep symetrical or projection will be off
# assuming square
in_size = cty.shape[0]
trim = 10 # percent of image
trim = int(np.around((trim / 100) * in_size, 0))

new_a = trim
new_b = in_size - trim

cty = cty[new_a:new_b, new_a:new_b].copy()
row = row[new_a:new_b, new_a:new_b].copy()
wat = wat[new_a:new_b, new_a:new_b].copy()


# dealing with unlabelled or multilabelled pixels
total = cty*1 + row*1 + wat*1

# nothing is unlabelled
assert (total == 0).sum() == 0


# for pixels that are marked as two layers, make them the preferred layer
# in the same order as above
coords_mult = np.argwhere(total > 1)

for coord in coords_mult:
    if wat[coord[0], coord[1]]:
        cty[coord[0], coord[1]] = False
        row[coord[0], coord[1]] = False
    elif cty[coord[0], coord[1]]:
        row[coord[0], coord[1]] = False
    else:
        print('problem with multi fill')

# everything is labelled only once
new_total = cty*1 + row*1 + wat*1

assert (new_total == 0).sum() == 0
assert (new_total == 1).sum() == new_total.shape[0] * new_total.shape[1]
assert (new_total > 1).sum() == 0

# define colours for water, canada, and other land
c_wat = [185, 225, 255, 255]
c_cty = [225, 245, 215, 255]
c_row = [240, 255, 240, 255]

img_wat = np.dstack([np.ones_like(wat) * wat] * 4) * c_wat
img_cty = np.dstack([np.ones_like(cty) * cty] * 4) * c_cty
img_row = np.dstack([np.ones_like(row) * row] * 4) * c_row

img_out = img_wat + img_cty + img_row


assert int(img_out.max()) <= 255

img_out = img_out / 255.0
img_out = img_out.copy()

assert img_out.max() == 1.0


# memory management
del cty
del row
del wat
del total
del new_total
del img_wat
del img_cty
del img_row



fig, ax = plt.subplots(dpi=dpi)
ax.imshow(img_out)




opath = ''
fname = f'./images/maps/{country}_lakes{lake_size}_rivers{river_size}_{dpi}dpi.png'
save = True

if save:
    plt.imsave(fname,
               img_out,
               dpi=dpi,
               )