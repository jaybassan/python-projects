# code that brute force initialises a three body system
# with random positions and velocities and then sums the
# total distance after a certain 
import numpy as np
import time
from utils import *
import pandas as pd

# mean and stdev of all parameters
p1_av = 0.0
p1_sd = 20.0
v1_av = 0.0
v1_sd = 10.0
m1_av = 30.0
m1_sd = 10.0

p2_av = 0.0
p2_sd = 20.0
v2_av = 0.0
v2_sd = 10.0
m2_av = 30.0
m2_sd = 10.0

p3_av = 0.0
p3_sd = 20.0
v3_av = 0.0
v3_sd = 10.0
m3_av = 30.0
m3_sd = 10.0

# time parameters
delta_t = 0.01
steps = 100_000

# how many attempts to save after. Allows easy ish keyboard interruption
iterations = 50_000

# seed the RNG for reproducibility
seed = int(time.time())
rng = np.random.default_rng(seed=seed)

# results dict
dict_results = {}

for n in range(1,4):
    dict_results[f'p{n}x'] = []
    dict_results[f'p{n}y'] = []
    dict_results[f'p{n}z'] = []
    dict_results[f'v{n}x'] = []
    dict_results[f'v{n}y'] = []
    dict_results[f'v{n}z'] = []
    dict_results[f'm{n}'] = []

dict_results['steps'] = []


# loop to perform the calculation
for i in range(iterations):
    p1_start = rng.normal(loc=p1_av, scale=p1_sd, size=3)
    v1_start = rng.normal(loc=v1_av, scale=v1_sd, size=3)
    m1 = rng.normal(loc=m1_av, scale=m1_sd, size=1)

    p2_start = rng.normal(loc=p1_av, scale=p2_sd, size=3)
    v2_start = rng.normal(loc=v1_av, scale=v2_sd, size=3)
    m2 = rng.normal(loc=m2_av, scale=m2_sd, size=1)

    p3_start = rng.normal(loc=p1_av, scale=p3_sd, size=3)
    v3_start = rng.normal(loc=v1_av, scale=v3_sd, size=3)
    m3 = rng.normal(loc=m3_av, scale=m3_sd, size=1)

	# set up parameters in tuple (mass, p_start, v_start)
    I1 = (
		m1,
		p1_start,
		v1_start
        )

    I2 = (
		m2,
		p2_start,
		v2_start
        )

    I3 = (
		m3,
		p3_start,
		v3_start
        )
    
	# run
    p = get_trajectories_limited(I1, I2, I3, delta_t=delta_t, steps=steps, max_rel=250, max_abs=500)
    p_start = (I1[1], I2[1], I3[1])

    # the loss is now the number of steps that arent nan
    num_steps_survived = (~np.isnan(p[0][:, 0])).sum()

    # add results to dict
    dict_results['p1x'].append(p1_start[0])
    dict_results['p1y'].append(p1_start[1])
    dict_results['p1z'].append(p1_start[2])
    dict_results['v1x'].append(v1_start[0])
    dict_results['v1y'].append(v1_start[1])
    dict_results['v1z'].append(v1_start[2])
    dict_results['m1'].append(m1[0])

    dict_results['p2x'].append(p2_start[0])
    dict_results['p2y'].append(p2_start[1])
    dict_results['p2z'].append(p2_start[2])
    dict_results['v2x'].append(v2_start[0])
    dict_results['v2y'].append(v2_start[1])
    dict_results['v2z'].append(v2_start[2])
    dict_results['m2'].append(m2[0])

    dict_results['p3x'].append(p3_start[0])
    dict_results['p3y'].append(p3_start[1])
    dict_results['p3z'].append(p3_start[2])
    dict_results['v3x'].append(v3_start[0])
    dict_results['v3y'].append(v3_start[1])
    dict_results['v3z'].append(v3_start[2])
    dict_results['m3'].append(m3[0])

    dict_results['steps'].append(num_steps_survived)

    # progress
    prop_done = (i+1)/iterations
    elapsed = time.time() - seed
    time_left = (elapsed / prop_done) - elapsed
    time_left = np.round(time_left / 60., 1)
    print(f'Done {i+1:,} of {iterations:,}. {time_left} minutes left.', end='\r')

# build df
df_out = pd.DataFrame(dict_results)

took = (time.time() - seed) / 60.0
took = int(np.around(took))
print(f'Finished {iterations:,} iterations, took {took:,} minutes.')



filename = f'./trajectories/seed{seed}-took{took}-iterations{iterations}.csv'

df_out.to_csv(filename, index=False)