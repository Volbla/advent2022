import numpy as np
from numpy import array
from itertools import count

from typing import Any
from nptyping import NDArray, Bool

with open("24.txt", "r", newline="\n") as f:
	inptext = f.read().splitlines()
example = """\
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
""".splitlines()

big_example = """\
#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".splitlines()

def main():
	characters = array(list(map(list, inptext)))
	directions = array(["^","v","<",">"])
	blizzards = directions[:,None,None] == characters[None, 1:-1, 1:-1]

	minutes = open_path(blizzards)
	print(minutes)

def open_path(blizzards_start:NDArray[Any, Bool]):
	blizzards = blizzards_start.copy()
	size_x, size_y = blizzards.shape[1:]
	movement = (-1, 1, -1, 1)
	axes = (0,0,1,1)

	# All possible current positions
	positions = np.zeros((size_x, size_y), dtype=bool)
	# Include a margin so the positions don't wrap around the edges like the blizzards do.
	walkable = np.zeros((4, size_x + 2, size_y + 2), dtype=bool)

	finale = (size_x - 1, size_y - 1)

	for minute in count(1):
		walkable.fill(False)
		walkable[:, 1:-1, 1:-1] = positions

		for i in range(4):
			blizzards[i] = np.roll(blizzards[i], movement[i], axis=axes[i])
			walkable[i] = np.roll(walkable[i], movement[i], axis=axes[i])
		has_blizzard = np.any(blizzards, axis=0)

		# First time entering the valley
		if not np.any(positions):
			positions[0,0] = True

		positions = (
			(positions |
			np.any(walkable[:, 1:-1, 1:-1], axis=0)) &
			~has_blizzard
		)

		# print(minute, np.count_nonzero(positions))
		if positions[finale]:
			break

	return minute + 1

if __name__ == "__main__":
	print()
	main()
