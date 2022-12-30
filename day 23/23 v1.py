import numpy as np
from numpy import array
from itertools import count

from nptyping import NDArray
from typing import Iterator

with open("23.txt", "r", newline="\n") as f:
	inptext = f.read().splitlines()

example = """\
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
""".splitlines()

smallexample = """\
.....
..##.
..#..
.....
..##.
.....
""".splitlines()

def main():
	elfgrid = array(list(map(list, inptext)))
	numpcoords = np.nonzero(elfgrid == "#")
	coords = array(tuple(zip(*reversed(numpcoords))))

	# 1
	_, new_coords = spread_out(coords, range(10))

	area = np.prod(
		np.max(new_coords, axis=0)
		- np.min(new_coords, axis=0) + 1
	)
	print(area - len(coords))

	# 2
	i, _ = spread_out(coords, count(1))
	print(i)


def spread_out(start_coords:NDArray, iterator:Iterator) -> tuple[int,NDArray]:
	coords = start_coords.copy()

	all_neighbors = array([[-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]])
	movement_order = array([[0,-1], [0,1], [-1,0], [1,0]])
	propositions = array([
		[[-1,-1], [0,-1], [1,-1]],	# North
		[[-1,1], [0,1], [1,1]],		# South
		[[-1,-1], [-1,0], [-1,1]],	# West
		[[1,-1], [1,0], [1,1]]		# East
	])

	potential = []
	for i in iterator:
		all_adjacent = coords[:, np.newaxis, :] + all_neighbors
		occupied = np.isin(packlong(all_adjacent), packlong(coords))
		want_to_move = np.any(occupied, axis=1)

		if not np.any(want_to_move):
			break

		for prop in propositions:
			three_points = coords[:, np.newaxis, :] + prop
			occupied = np.isin(packlong(three_points), packlong(coords))
			tempted = ~np.any(occupied, axis=1) & want_to_move

			for already_decided in potential:
				tempted &= ~already_decided

			potential.append(tempted)

		# Only elves moving along the same axis can bump into each other.
		for axis in range(2):
			dir1, dir2 = np.flatnonzero(movement_order[:,axis])

			try_move1 = packlong(coords[potential[dir1]] + movement_order[dir1])
			try_move2 = packlong(coords[potential[dir2]] + movement_order[dir2])

			cant_move1 = np.isin(try_move1, try_move2)
			cant_move2 = np.isin(try_move2, try_move1)

			does_move1 = np.flatnonzero(potential[dir1])[~cant_move1]
			does_move2 = np.flatnonzero(potential[dir2])[~cant_move2]

			coords[does_move1] += movement_order[dir1]
			coords[does_move2] += movement_order[dir2]

		propositions = np.roll(propositions, -1, axis=0)
		movement_order = np.roll(movement_order, -1, axis=0)
		potential = []

	return i, coords


def packlong(arr:NDArray) -> NDArray:
	"""Comparing sub-arrays in numpy is not worth it.
	Packing the last axis (the coordinates) into a single number instead.
	"""

	uint_array = arr.astype(np.uint32).astype(np.uint64)
	uint_array[...,0] <<= 32
	return np.sum(uint_array, axis=-1)

# Not used
def unpacklong(x:NDArray) -> NDArray:
	byte_mask = np.full(
		(1,) * x.ndim + (2,),
		2 ** 32 - 1,
		dtype=np.uint64)

	byte_mask[...,0] <<= 32
	uint_array = x[:,np.newaxis] & byte_mask
	uint_array[...,0] >>= 32

	return uint_array.astype(np.int32)

if __name__ == "__main__":
	print()
	main()
