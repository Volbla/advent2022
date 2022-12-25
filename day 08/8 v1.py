from itertools import product
import numpy as np

with open("8.txt", "r", newline="\n") as f:
	trees = np.array(
		[[int(digit)
		for digit in line.strip()]
		for line in f]
	)
y, x = trees.shape

# 1
visible = np.zeros_like(trees, dtype=bool)
visible[0,:] = visible[:,0] = visible[-1,:] = visible[:,-1] = True
for j, i in product(range(1, x-1), range(1, y-1)):
	tree = trees[i,j]
	visible[i,j] = (
		tree > max(trees[i, :j]) or
		tree > max(trees[i, j+1:]) or
		tree > max(trees[:i, j]) or
		tree > max(trees[i+1:, j])
	)
print(sum(visible.flatten()))

# 2
def score_for_axis(line, index, edgeindex):
	tallindex = np.concatenate((
		[0],
		np.flatnonzero(line >= line[index]),
		[edgeindex]
	))
	dist = np.abs(tallindex - index)
	i = np.flatnonzero(dist == 0)[0]
	return dist[i + 1] * dist[i - 1]

scores = np.zeros_like(trees, dtype=int)
for j, i in product(range(1, x-1), range(1, y-1)):
	tree = trees[i,j]
	scores[i,j] = (
		score_for_axis(trees[i,:], j, x - 1) *
		score_for_axis(trees[:,j], i, y - 1)
	)
print(max(scores.flatten()))
print(np.unravel_index(np.argmax(scores), scores.shape))
