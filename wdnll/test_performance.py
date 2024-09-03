# script to test performance of different functions in the utils 
import time
import numpy as np
from matplotlib import pyplot as plt


from utils import *


max=10_000_000
step=1_000_000

caps = [i for i in range(10, max, step)]
times = []

for idx, c in enumerate(caps):
    tstart = time.time()
    primes = primes_below(c)

    took = time.time() - tstart
    times.append(took)

    print(f'Done {idx+1:,} of {len(caps):,}', end='\r')

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10,10))

ax.scatter(
    caps,
    times,
    marker='.',
    c='b',
    )

ax.set_xlabel('max. prime size')
ax.set_ylabel('time / s')



plt.tight_layout()
plt.show()