# is there a way to do this more efficiently while also counting the number of iterations that
# a point survives for?

import numpy as np
import itertools
import matplotlib.pyplot as plt

xmin = -4.0
xmax = 4.0
ymin = -4.0
ymax = 4.0

num_points = 10000

re = np.linspace(xmin, xmax, num_points)
im = np.linspace(ymin, ymax, num_points)

c = [complex(pair[0], pair[1]) for pair in itertools.product(re, im)]
c = np.array(c)

# array to hold the results
a = np.zeros_like(c)
list_out = np.zeros((num_points ** 2), dtype=int)


num_iterations = 5000

for z in range(num_iterations):
    # square and self add
    a = (a ** 2) + c

    # get the pixels that escaped the bound this iteration
    out_this_round = abs(a) > 2.0

    # set these points in the out list to the current iteration
    list_out[out_this_round] = z

    # set the points in the matrix to 0,0 so they dont get caught again
    a[out_this_round] = complex(0, 0)


    print(f'Done {z+1:,} of {num_iterations:,}', end='\r')


img = list_out.reshape((num_points, num_points), order='f')


# save the array
np.save(f'./data/{num_points}x{num_points}-{num_iterations}iterations.npy', img)

