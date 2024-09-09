# goal is to find three-body starting conditions that result in, at some point, the bodies being in their exact same starting positions
# most aesthetically pleasing would be if they all start at the same point.
# obv not realistic

import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
# plt.style.use('dark_background')

def accelerations(p1, p2, p3, m_1, m_2, m_3):
	"""
	function to calculate the derivatives of x, y, and z
	given 3 object and their locations according to Newton's laws
	"""
	planet_1_dv = -9.8 * m_2 * (p1 - p2)/(np.sqrt(np.sum([i**2 for i in p1 - p2]))**3) - 9.8 * m_3 * (p1 - p3)/(np.sqrt(np.sum([i**2 for i in p1 - p3]))**3)

	planet_2_dv = -9.8 * m_3 * (p2 - p3)/(np.sqrt(np.sum([i**2 for i in p2 - p3]))**3) - 9.8 * m_1 * (p2 - p1)/(np.sqrt(np.sum([i**2 for i in p2 - p1]))**3)

	planet_3_dv = -9.8 * m_1 * (p3 - p1)/(np.sqrt(np.sum([i**2 for i in p3 - p1]))**3) - 9.8 * m_2 * (p3 - p2)/(np.sqrt(np.sum([i**2 for i in p3 - p2]))**3)

	return planet_1_dv, planet_2_dv, planet_3_dv


def get_trajectories(I1, I2, I3, delta_t=0.01, steps=50000):
	# unpack mass, starting position and velocity
	m1, p1_start, v1_start = I1
	m2, p2_start, v2_start = I2
	m3, p3_start, v3_start = I3



	# initialize solution array
	p1 = np.array([[0.,0.,0.] for i in range(steps)])
	v1 = np.array([[0.,0.,0.] for i in range(steps)])

	p2 = np.array([[0.,0.,0.] for j in range(steps)])
	v2 = np.array([[0.,0.,0.] for j in range(steps)])

	p3 = np.array([[0.,0.,0.] for k in range(steps)])
	v3 = np.array([[0.,0.,0.] for k in range(steps)])




	# starting points
	p1[0], p2[0], p3[0] = p1_start, p2_start, p3_start

	v1[0], v2[0], v3[0] = v1_start, v2_start, v3_start



	# evolution of the system
	for i in range(steps-1):
		
		# calculate derivatives
		dv1, dv2, dv3 = accelerations(p1[i], p2[i], p3[i], m1, m2, m3)

		# update velocities
		v1[i + 1] = v1[i] + dv1 * delta_t
		v2[i + 1] = v2[i] + dv2 * delta_t
		v3[i + 1] = v3[i] + dv3 * delta_t

		# update positions
		p1[i + 1] = p1[i] + v1[i] * delta_t
		p2[i + 1] = p2[i] + v2[i] * delta_t
		p3[i + 1] = p3[i] + v3[i] * delta_t

	return p1, p2, p3
		


def get_best_distance(p, p_start, min_frames=100):
	p1, p2, p3 = p
	p1_start, p2_start, p3_start = p_start


	# get the squared distance from each planets starting position
	d1 = ((p1 - p1_start) ** 2).sum(axis=1)
	d2 = ((p2 - p2_start) ** 2).sum(axis=1)
	d3 = ((p3 - p3_start) ** 2).sum(axis=1)

	# get the minimum aggregate distance in the points AFTER min frames elapsed
	d = d1 + d2 + d3
	out_val = d[100:].min()

	ever_better = np.argmin(d[min_frames]) == 0

	return out_val, ever_better

def loss(p, p_start):
	# loss function that looks to MINIMIZE the ABSOLUTE total distance 
	# of the planet's path on each axis, allowing a wild path as long as its centred
	p1, p2, p3 = p
	p1_start, p2_start, p3_start = p_start

	d1 = (p1 - p1_start).sum(axis=0) ** 2
	d2 = (p2 - p2_start).sum(axis=0) ** 2
	d3 = (p3 - p3_start).sum(axis=0) ** 2

	d1 = d1.sum()
	d2 = d2.sum()
	d3 = d3.sum()

	d = np.sqrt((d1 + d2 + d3))

	return d

# now run a bunch of different randomish starting conditions
# and see if any come close to the goal.
# just change the y and z velocity of the second planet to start
num_to_run = 500
runs = [r for r in range(num_to_run)]
rng = np.random.default_rng(123)


p2y_vels = []
p2z_vels = []
losses = []

for idx, run in enumerate(runs):
	# get some random values for y and z velocities
	v2y = rng.uniform(low=-10.0, high=10.0)
	v2z = rng.uniform(low=-10.0, high=10.0)

	# set up parameters in tuple (mass, p_start, v_start)
	I1 = (
		10,
		np.array([-10, 10, -11]),
		np.array([-3, 1, 0])
	)

	I2 = (
		20,
		np.array([0, 0, 0]),
		np.array([0, v2y, v2z])
	)

	I3 = (
		30,
		np.array([10, 10, 12]),
		np.array([3, 0, 0])
	)


	# run
	p = get_trajectories(I1, I2, I3)
	p_start = (I1[1], I2[1], I3[1])

	# get the best distance after 100 frames,
	# and whether is there ever a better timestep or is this just the best because its the earliest
	loss_traj = loss(p, p_start)
	

	# add to lists
	p2y_vels.append(v2y)
	p2z_vels.append(v2z)
	losses.append(loss_traj)

	# print progress
	print(f'Done {idx+1:,} of {num_to_run:,}', end='\r')

fig, ax = plt.subplots(ncols=1, figsize=(10,10))

sc0 = ax.scatter(p2y_vels, p2z_vels, marker='.', c=losses, cmap='magma_r', s=500, alpha=0.8)
fig.colorbar(sc0, ax=ax)


plt.tight_layout()
plt.show()


# seems like this wont be fruitful. Will try and implement some kind of SGD
# using similar loss functions