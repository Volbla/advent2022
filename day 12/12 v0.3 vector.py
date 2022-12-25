import numpy as np
from numpy.typing import NDArray
from PIL import Image

with open("12.txt", "r", newline="\n", encoding="ascii") as f:
	heightmap = np.array([[ord(c) for c in s] for s in f.read().splitlines()])

start = np.nonzero(heightmap == ord("S"))
end = np.nonzero(heightmap == ord("E"))
heightmap[start] = ord("a")
heightmap[end] = ord("z")

hx5 = np.repeat(heightmap, 5, axis=1)
hxy5 = np.repeat(hx5, 5, axis=0)
start5 = (start[0] * 5, start[1] * 5)
end5 = (end[0] * 5, end[1] * 5)

pic = ((hxy5 - ord("a")) / 25) ** (1 / 2.2) * 255
greypic = pic.astype(np.uint8)

neighbor_diff = np.stack((
	np.roll(hxy5, 1, axis=0),
	np.roll(hxy5, 1, axis=1),
	np.roll(hxy5, -1, axis=1),
	np.roll(hxy5, -1, axis=0),
)) - hxy5
neighbor_diff[0,0,:] = neighbor_diff[0,1,:]
neighbor_diff[1,:,0] = neighbor_diff[1,:,1]
neighbor_diff[2,:,-1] = neighbor_diff[2,:,-2]
neighbor_diff[3,-1,:] = neighbor_diff[3,-2,:]

up1 = np.any(neighbor_diff == 1, axis=0)
downlots = np.any(neighbor_diff < -1, axis=0)
curheight = greypic == greypic[start5]

edges = np.tile(greypic[:,:,np.newaxis], (1,1,3))
edges[curheight] = [50, 50, 200]
edges[downlots & curheight] = [200, 200, 100]
edges[up1 & curheight] = [100, 220, 140]

hx10 = np.repeat(edges, 2, axis=1)
hxy10 = np.repeat(hx10, 2, axis=0)

Image.fromarray(hxy10, mode="RGB").show()
