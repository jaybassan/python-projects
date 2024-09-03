import numpy as np
import time
from utils import factor_vector_lil
import umap
from matplotlib import pyplot as plt

tstart = time.time()

# get the factor matrix up to n
n = 5_000_000
X = factor_vector_lil(n) 

# embed with UMAP
embedding = umap.UMAP(metric='cosine', n_epochs=500, verbose=True).fit_transform(X)

# save for later
np.savez(f'{n}_pts.npz', embedding=embedding)

# print time
took = time.time() - tstart
took = int(np.around(took/60.0, 0))
print(f'Finished {n:,} numbers, took {took:,} minutes')

# get the colormap
cmap = plt.get_cmap('magma')
c = cmap(np.linspace(0, 1, n))

# and save the image
fig = plt.figure(figsize=(8,8))
fig.patch.set_facecolor('black')
plt.scatter(
    embedding[:,0], embedding[:,1],
    marker='.',
    s=0.5,
    facecolor=c,
    edgecolor='none',
    )

plt.axis("off")
plt.savefig(f"{n}.png", dpi=600)




