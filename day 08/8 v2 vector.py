import numpy as np
new = np.newaxis

with open("8.txt", "r", newline="\n") as f:
	trees = np.array(
		[[int(digit)
		for digit in line.strip()]
		for line in f]
	)
# Since the grid is square we can make some shortcuts when defining arrays.
y, x = trees.shape

# Stack the grid in a new "depth" dimension.
# Compare it against both the horizontal and vertical axes.
depthstack = np.tile(trees[new,:,:], [x,1,1])
xcomp = np.swapaxes(depthstack, 0, 2)
ycomp = np.swapaxes(depthstack, 0, 1)

# Masks for all trees tall enough to block the view.
EW_tallmask = depthstack <= xcomp
NS_tallmask = depthstack <= ycomp

# Indexing visible trees in the depth-axis.
depthindex = np.tile(np.arange(x)[:,new,new], [1,x,x])
# Our own tree's x-coordinate.
EW_index = np.swapaxes(depthindex, 0, 2)
# Our own tree's y-coordinate.
NS_index = np.swapaxes(depthindex, 0, 1)

# Masks for each viewdirection.
E_viewmask = depthindex > EW_index
W_viewmask = depthindex < EW_index
N_viewmask = depthindex < NS_index
S_viewmask = depthindex > NS_index

# Select the valid index in the depth-axis that is closest to the tree's position.
# The difference with the tree's own index is the distance.
E_dist = np.amin(depthindex, axis=0, where=EW_tallmask & E_viewmask, initial=x - 1) - EW_index
S_dist = np.amin(depthindex, axis=0, where=NS_tallmask & S_viewmask, initial=x - 1) - NS_index
W_dist = EW_index - np.amax(depthindex, axis=0, where=EW_tallmask & W_viewmask, initial=0)
N_dist = NS_index - np.amax(depthindex, axis=0, where=NS_tallmask & N_viewmask, initial=0)

viewscore = E_dist * S_dist * W_dist * N_dist
prime_tree = np.amax(viewscore.flat)

print(prime_tree)
