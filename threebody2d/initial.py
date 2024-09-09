import numpy as np
import matplotlib.pyplot as plt
from utils import *

I1 = (
    10,
    np.array([0., 0.]),
    np.array([0., 0.])
)

I2 = (
    10,
    np.array([0., 1.]),
    np.array([0, 0])
)

I3 = (
    10,
    np.array([0., -1]),
    np.array([0, 0])
)



t1, t2, t3 = get_trajectories(I1, I2, I3)
                              
plt.scatter(t1[:, 0], t1[:, 1])
plt.scatter(t2[:, 0], t2[:, 1])
plt.scatter(t3[:, 0], t3[:, 1])

plt.show()