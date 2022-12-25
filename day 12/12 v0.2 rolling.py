import numpy as np
from PIL import Image
from numpy.typing import NDArray
BoolArray = NDArray[np.bool_]

with open("12.txt", "r", newline="\n", encoding="ascii") as f:
	heightmap = np.array([[ord(c) for c in s] for s in f.read().splitlines()])
start = heightmap == ord("S")
end = heightmap == ord("E")
heightmap[start] = ord("a")
heightmap[end] = ord("z")

def main():
	heights = [heightmap == x for x in range(ord("a"), ord("z"))]
	subgoals = [stepup_places(x) for x in heights]
	allgoals = np.logical_or.reduce(subgoals)

	draw_path(allgoals)
	# draw_mask(stepup_places(heights[2]))
	# draw_mask(np.concatenate(subgoals))

def expand_into_neighbors(area:BoolArray) -> BoolArray:
	up = np.roll(area, -1, axis=0)
	left = np.roll(area, -1, axis=1)
	right = np.roll(area, 1, axis=1)
	down = np.roll(area, 1, axis=0)
	up[-1,:] = False
	left[:,-1] = False
	right[:,0] = False
	down[0,:] = False

	return up | left | right | down

def stepup_places(area:BoolArray) -> BoolArray:
	oldheight = heightmap[area][0]
	newheight_mask = heightmap == oldheight + 1

	neighbors = expand_into_neighbors(area) != area
	new_heights = neighbors & newheight_mask

	old_neighbors = expand_into_neighbors(new_heights) != new_heights

	return old_neighbors & area

def mask_connected_flat(area:BoolArray, offset:int=0) -> BoolArray:
	heightmask = heightmap == heightmap[area][0] + offset

	result = expand_into_neighbors(area) & heightmask
	while not np.array_equal(result, anotha := expand_into_neighbors(result) & heightmask):
		result |= anotha

	return result

def draw_mask(area:BoolArray) -> None:
	scale = 8

	greypic = (~area).astype(np.uint8) * 255
	xstretch = np.repeat(greypic, scale, axis=1)
	xystretch = np.repeat(xstretch, scale, axis=0)

	# y, x = area.shape
	# xystretch[:, np.arange(x) * scale - 1] = 128
	# xystretch[np.arange(y) * scale - 1, :] = 128

	Image.fromarray(xystretch, mode="L").show()

def draw_path(pathmask:BoolArray) -> None:
	pic = ((heightmap - ord("a")) / 25) ** (1 / 2.2) * 255
	greypic = pic.astype(np.uint8)
	colorpic = np.tile(greypic[:,:,np.newaxis], [1,1,3])

	colorpic[pathmask] = [80, 180, 80]

	# Scaling
	a = np.repeat(colorpic, 10, axis=1)
	b = np.repeat(a, 10, axis=0)
	Image.fromarray(b, mode="RGB").show()

if __name__ == "__main__":
	print()
	main()
