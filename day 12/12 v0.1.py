import numpy as np
from numpy.typing import NDArray
from PIL import Image
from time import sleep

with open("12.txt", "r", newline="\n", encoding="ascii") as f:
	# heightmap = np.array(list(map(list, f.read().splitlines())))
	heightmap = np.array([[ord(c) for c in s] for s in f.read().splitlines()])

def neighbors(pos:tuple[NDArray]) -> NDArray[np.bool_]:
	# up, down, left, right
	ydir = np.array([-1,1,0,0])
	xdir = np.array([0,0,-1,1])

	ymax, xmax = heightmap.shape
	edge_mask = np.array([
		pos[0] != 0,
		pos[0] != ymax - 1,
		pos[1] != 0,
		pos[1] != xmax - 1
		], dtype=bool
	).squeeze()

	available_slots = (pos[0] + ydir[edge_mask], pos[1] + xdir[edge_mask])

	mask = np.zeros_like(heightmap, dtype=bool)
	mask[available_slots] = True
	return mask

def walkable_from(pos:tuple[NDArray]) -> NDArray[np.bool_]:
	y, x = neighbors(pos)
	slope_mask = heightmap[(y,x)] - heightmap[pos] <= 1
	return slope_mask
	good_slopes = (y[slope_mask], x[slope_mask])
	return good_slopes

def mask_this_level(pos:tuple[NDArray]) -> NDArray[np.bool_]:
	heightmask = heightmap == heightmap[pos]

	confirmed = []
	new = [pos]
	newnew = []

	while new:
		for p in new:
			neighbormask = neighbors(p)
			prancable = np.nonzero(neighbormask & heightmask)
			for spot in zip(*prancable):
				if spot not in confirmed:
					newnew.append(spot)
		confirmed += new
		new.clear()
		new += newnew
		newnew.clear()

	thisman = np.zeros_like(heightmap, dtype=bool)
	for p in confirmed:
		thisman[p] = True
	return thisman

def stepups(level:NDArray[np.bool_]) -> NDArray[np.bool_]:
	next_height = heightmap[level][0] + 1
	heightmask = heightmap == next_height

	confirmed = []
	new = []
	newnew = []

	for p in zip(*np.nonzero(level)):
		neighbormask = neighbors(p)
		prancable = np.nonzero(neighbormask & heightmask)
		for spot in zip(*prancable):
			if spot not in new:
				new.append(spot)

	while new:
		# for thang in (confirmed, new):
		# 	print(thang[-45:])
		# print("yes")
		for p in new:
			neighbormask = neighbors(p)
			prancable = np.nonzero(neighbormask & heightmask)
			for spot in zip(*prancable):
				if spot not in confirmed and spot not in new and spot not in newnew:
					newnew.append(spot)
		confirmed += new
		new.clear()
		new += newnew
		newnew.clear()

	thisman = np.zeros_like(heightmap, dtype=bool)
	for p in confirmed:
		thisman[p] = True
	return thisman

def draw_mask(area:NDArray[np.bool_]) -> None:
	greypic = 255 - area.astype(np.uint8) * 255
	a = np.repeat(greypic, 10, axis=1)
	b = np.repeat(a, 10, axis=0)

	Image.fromarray(b, mode="L").show()

start = np.nonzero(heightmap == ord("S"))
end = np.nonzero(heightmap == ord("E"))
heightmap[start] = ord("a")
heightmap[end] = ord("z")

lvl0 = mask_this_level(start)
lvl1 = stepups(lvl0)
lvl2 = stepups(lvl1)
draw_mask(lvl2)
