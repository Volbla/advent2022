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

	# 1
	minutes = time_to_navigate(blizzards, 1)
	print(minutes)

	# 2
	minutes = time_to_navigate(blizzards, 3)
	print(minutes)

def time_to_navigate(blizzards_start:NDArray[Any, Bool], roundtrips:int) -> int:
	blizzards = blizzards_start.copy()
	size_x, size_y = blizzards.shape[1:]
	movement = (-1, 1, -1, 1)
	axes = (0,0,1,1)

	# All possible current positions
	positions = np.zeros((size_x, size_y), dtype=bool)
	# Include a margin so the positions don't wrap around the edges like the blizzards do.
	walkable = np.zeros((4, size_x + 2, size_y + 2), dtype=bool)

	trips = 0
	start = (0, 0)
	goal = (size_x - 1, size_y - 1)

	for minute in count(1):
		walkable.fill(False)
		walkable[:, 1:-1, 1:-1] = positions

		for i in range(4):
			blizzards[i] = np.roll(blizzards[i], movement[i], axis=axes[i])
			walkable[i] = np.roll(walkable[i], movement[i], axis=axes[i])
		has_blizzard = np.any(blizzards, axis=0)

		# When entering the valley
		if not np.any(positions):
			positions[start] = True

		positions = (
			(positions |
			np.any(walkable[:, 1:-1, 1:-1], axis=0)) &
			~has_blizzard
		)

		# print(minute, np.count_nonzero(positions))
		if positions[goal]:
			trips += 1
			if trips == roundtrips:
				break

			# Account for blizzard movement when exiting the valley
			for i in range(4):
				blizzards[i] = np.roll(blizzards[i], movement[i], axis=axes[i])
			positions.fill(False)
			start, goal = goal, start

	return minute + roundtrips

if __name__ == "__main__":
	print()
	main()
