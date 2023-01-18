import numpy as np
from math import inf
from PIL import Image

# ///// TYPING SHIT /////

from typing import Callable, Sequence, overload, Any
from nptyping import NDArray, Int, Bool

# Subsequences contain parallel y- and x-coordinates.
# Compatible with numpy simultaneous indexing.
onecoord = tuple[int,...] | NDArray[Any, Int]
Indices = tuple[onecoord, onecoord]

# Compatible with regular iteration over individual coordinates.
Point = tuple[int, int]
Coordinates = Sequence[Point]

BoolMask = NDArray[Any, Bool]

@overload
def transpose(tuptup:Indices) -> Coordinates: ...
@overload
def transpose(tuptup:Coordinates) -> Indices: ...

# ///// END TYPING SHIT /////

def transpose(tuptup):
	# Transforms between the two coordinate types.
	return tuple(zip(*tuptup))

with open("12.txt", "r", newline="\n", encoding="ascii") as f:
	heightmap = np.array([[ord(c) for c in s] for s in f.read().splitlines()])
start:Point = transpose(np.nonzero(heightmap == ord("S")))[0]
end:Point = transpose(np.nonzero(heightmap == ord("E")))[0]
heightmap[start] = ord("a")
heightmap[end] = ord("z")

def main():
	def lower_estimate(p:Point) -> int:
		# Straight manhattan distance.
		return abs(end[0] - p[0]) + abs(end[1] - p[1])

	# 1
	path = A_Star(start, end, lower_estimate)
	if path is None:
		print("End was unreachable")
		return
	# print(len(path) - 1)
	# draw_path(path)
	# return

	# 2
	from_a = stepupable(transpose(np.nonzero(heightmap == ord("a"))))
	print(len(from_a))

	for s in from_a:
		short_path = A_Star(s, end, lower_estimate)
		if short_path is not None and len(short_path) < len(path):
			path = short_path

	print(len(path) - 1)
	draw_path(path)

def stepupable(area:Coordinates) -> Coordinates:
	old_height = heightmap[area[0]]
	mask = np.zeros(len(area), dtype=bool)

	for i, p in enumerate(area):
		neigh = neighbors(p)
		heights = heightmap[neigh]
		mask[i] = old_height + 1 in heights

	iarea = transpose(area)
	npy, npx = np.array(iarea[0]), np.array(iarea[1])
	able = (npy[mask], npx[mask])

	return transpose(able)

def A_Star(start:Point, goal:Point, h:Callable) -> Coordinates|None:
	openSet:set[Point] = {start,}

	cameFrom:dict[Point, Point] = {}

	gScore:dict[Point, int] = {}
	gScore[start] = 0

	fScore:dict[Point, int] = {}
	fScore[start] = h(start)

	while openSet:
		current = sorted(list(openSet), key=lambda x: fScore[x])[0]
		if current == goal:
			return reconstruct_path(cameFrom, current)

		openSet.remove(current)
		for neighbor in walkable_from(current):
			tentative_gScore = gScore[current] + 1

			if tentative_gScore < gScore.get(neighbor, inf):
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore
				fScore[neighbor] = tentative_gScore + h(neighbor)

				if neighbor not in openSet:
					openSet.add(neighbor)

	# Open set is empty but goal was never reached
	return None

def reconstruct_path(cameFrom:dict[Point, Point], current:Point) -> Coordinates:
	total_path = [current]

	while current in cameFrom.keys():
		current = cameFrom[current]
		total_path.append(current)

	total_path.reverse()
	return total_path

def neighbors(pos:Point) -> Indices:
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
	return available_slots

def walkable_from(pos:Point) -> Coordinates:
	y, x = neighbors(pos)
	slope_mask = heightmap[(y,x)] - heightmap[pos] <= 1
	walkable = (y[slope_mask], x[slope_mask])
	return transpose(walkable)

def draw_path(path:Coordinates) -> None:
	pic = ((heightmap - ord("a")) / 25) ** (1 / 2.2) * 255
	greypic = pic.astype(np.uint8)
	colorpic = np.tile(greypic[:,:,np.newaxis], [1,1,3])

	pathmask = np.zeros_like(heightmap, dtype=bool)
	pathmask[transpose(path)] = True
	colorpic[pathmask] = [80, 180, 80]

	# Scaling
	a = np.repeat(colorpic, 10, axis=1)
	b = np.repeat(a, 10, axis=0)
	Image.fromarray(b, mode="RGB").show()

if __name__ == "__main__":
	print()
	main()
