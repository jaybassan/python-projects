import numpy as np
def distance(p1, p2, axis=1):
	return np.sqrt(((p1 - p2) ** 2).sum(axis=axis))


def acceleration(p1, p2, p3, m1, m2, m3, G=1e10):
    force12 = G * m1 * m2 / (p1 - p2) ** 2
    force23 = G * m2 * m3 / (p2 - p3) ** 2
    force13 = G * m1 * m3 / (p1 - p3) ** 2
    
    dv1 = force12 + force13
    dv2 = -force12 + force23
    dv3 = -force23 - force13
    
    return dv1, dv2, dv3




def get_trajectories(I1, I2, I3, delta_t=0.01, steps=50000):
	# unpack mass, starting position and velocity
	m1, p1_start, v1_start = I1
	m2, p2_start, v2_start = I2
	m3, p3_start, v3_start = I3



	# initialize solution array
	p1 = np.array([[0., 0.] for i in range(steps)])
	v1 = np.array([[0., 0.] for i in range(steps)])
	
	p2 = np.array([[0., 0.] for j in range(steps)])
	v2 = np.array([[0., 0.] for j in range(steps)])
	
	p3 = np.array([[0., 0.] for k in range(steps)])
	v3 = np.array([[0., 0.] for k in range(steps)])




	# starting points
	p1[0], p2[0], p3[0] = p1_start, p2_start, p3_start

	v1[0], v2[0], v3[0] = v1_start, v2_start, v3_start



	# evolution of the system
	for i in range(steps-1):
		
		# calculate derivatives
		dv1, dv2, dv3 = acceleration(p1[i], p2[i], p3[i], m1, m2, m3)

		# update velocities
		v1[i + 1] = v1[i] + dv1 * delta_t
		v2[i + 1] = v2[i] + dv2 * delta_t
		v3[i + 1] = v3[i] + dv3 * delta_t

		# update positions
		p1[i + 1] = p1[i] + v1[i] * delta_t
		p2[i + 1] = p2[i] + v2[i] * delta_t
		p3[i + 1] = p3[i] + v3[i] * delta_t

	return p1, p2, p3
