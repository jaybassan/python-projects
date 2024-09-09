# helper functions for learning
import numpy as np

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




def get_trajectories_limited(I1, I2, I3, delta_t=0.01, steps=100000, max_rel=500, max_abs=1000):
	# stops the analysis as soon as any planet is outside of the +/- max in any dimension 
	# TODO include distance from eachother as well as / instead of absolute
	# TODO make each dimension max independent
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

		# check if any two planets are too far from eachother
		d12 = ((p1[i + 1] - p2[i + 1]) ** 2).sum() ** 0.5
		d23 = ((p2[i + 1] - p3[i + 1]) ** 2).sum() ** 0.5
		d13 = ((p1[i + 1] - p3[i + 1]) ** 2).sum() ** 0.5

		if d12 > max_rel or d13 > max_rel or d13 > max_rel:
			# make all following entries in all positions NaN
			p1[i + 2:] = np.nan
			p2[i + 2:] = np.nan
			p3[i + 2:] = np.nan

			# exit
			break


		# check if any planet is outside of the bounding box
		p1_check = abs(p1[i + 1]).max() > max_abs
		p2_check = abs(p2[i + 1]).max() > max_abs
		p3_check = abs(p3[i + 1]).max() > max_abs

		if p1_check or p2_check or p3_check:
			# make all following entries in all positions NaN
			p1[i + 2:] = np.nan
			p2[i + 2:] = np.nan
			p3[i + 2:] = np.nan

			# exit
			break



	return p1, p2, p3







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


def df_to_input(df):
	# unpack one line of a dataframe into the In vectors 
	m1 = df['m1'].item()
	m2 = df['m2'].item()
	m3 = df['m3'].item()

	p1 = np.array([
		df['p1x'].item(),
		df['p1y'].item(),
		df['p1z'].item(),
	])

	p2 = np.array([
		df['p2x'].item(),
		df['p2y'].item(),
		df['p2z'].item(),
	])

	p3 = np.array([
		df['p3x'].item(),
		df['p3y'].item(),
		df['p3z'].item(),
	])
	v1 = np.array([
		df['v1x'].item(),
		df['v1y'].item(),
		df['v1z'].item(),
	])

	v2 = np.array([
		df['v2x'].item(),
		df['v2y'].item(),
		df['v2z'].item(),
	])

	v3 = np.array([
		df['v3x'].item(),
		df['v3y'].item(),
		df['v3z'].item(),
	])

	I1 = (m1, p1, v1)
	I2 = (m2, p2, v2)
	I3 = (m3, p3, v3)

	return I1, I2, I3


def sgd2d(v2y, v2z, learn_rate=0.1, random_state=None):
    """
    Stoichastic gradient descent to update initial guesses of parameters
    keeping it 2d for now so can visualise easier.
    """
	# Initializing the random number generator
    seed = None if random_state is None else int(random_state)
    rng = np.random.default_rng(seed=seed)
	
    # get a 