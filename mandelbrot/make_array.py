# is there a way to do this more efficiently while also counting the number of iterations that
# a point survives for?

import numpy as np
import itertools
import matplotlib.pyplot as plt

xmin = -2.5
xmax = 2.5
ymin = -2.5
ymax = 2.5

num_points = 2 ** 14

re = np.linspace(xmin, xmax, num_points)
im = np.linspace(ymin, ymax, num_points)

c = [complex(pair[0], pair[1]) for pair in itertools.product(re, im)]
c = np.array(c)

# array to hold the results
a = np.zeros_like(c)
list_out = np.zeros((num_points ** 2), dtype=int)


num_iterations = 2 ** 10

for z in range(1, num_iterations+1):
    # square and self add
    a = (a ** 2) + c

    # get the pixels that escaped the bound this iteration
    out_this_round = abs(a) > 2.0

    # set these points in the out list to the current iteration
    list_out[out_this_round] = z

    # set the points in the matrix to 0,0 so they dont get caught again
    c[out_this_round] = complex(0, 0)


    print(f'Done {z:,} of {num_iterations:,}', end='\r')


img = list_out.reshape((num_points, num_points), order='f')

# points that are 0 in the image never escaped the bound and are in the M set for this number of iterations.
# set to indicate and make visualisation easier
img[img==0] = num_iterations+1


# save the array
np.save(f'./data/{num_points}x{num_points}-{num_iterations}iterations.npy', img)

