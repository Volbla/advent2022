import numpy as np
from itertools import cycle, count

from typing import Sequence

with open("17.txt", "r", newline="\n") as f:
	jets = [[1,0] if char == ">" else [-1,0] for char in f.read().strip()]
# Site example
# jets = [[1,0] if char == ">" else [-1,0] for char in ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]

shapes = (
	np.array([[0,0], [1,0], [2,0], [3,0]]),
	np.array([[1,0], [0,1], [1,1], [2,1], [1,2]]),
	np.array([[0,0], [1,0], [2,0], [2,1], [2,2]]),
	np.array([[0,0], [0,1], [0,2], [0,3]]),
	np.array([[0,0], [1,0], [0,1], [1,1]])
)

def main():
	tower = np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0]])
	jet = cycle(jets)
	shape = cycle(shapes)

	for _ in range(2022):
		block = next(shape).copy()
		block += [2, max(tower[:,1]) + 4]

		while True:
			movement = block + next(jet)
			is_blocked = (
				any(movement[:,0] == -1) or
				any(movement[:,0] == 7) or
				any_in(movement, tower)
			)
			if not is_blocked:
				block = movement

			movement = block + [0,-1]
			if not any_in(movement, tower):
				block = movement
				continue

			# Block landed
			tower = np.concatenate((tower, block))
			break

	print(max(tower[:,1]))

def any_in(a, b) -> bool:
	"""Compares all combinations of sub-arrays (coordinates)."""
	for x in a:
		coord_match = x == b
		pixel_match = np.all(coord_match, axis=1)
		if any(pixel_match):
			return True
	return False

if __name__ == "__main__":
	print()
	main()
