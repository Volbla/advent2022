import numpy as np
from itertools import cycle

from nptyping import NDArray

with open("17.txt", "r", newline="\n") as f:
	jets = [np.array([1,0]) if char == ">" else np.array([-1,0]) for char in f.read().strip()]
cache = "fromdata.npy"

# Site example
# jets = [[1,0] if char == ">" else [-1,0] for char in ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]
# cache = "fromexample.npy"

shapes = (
	np.array([[0,0], [1,0], [2,0], [3,0]]),
	np.array([[0,1], [1,0], [1,1], [1,2], [2,1]]),
	np.array([[0,0], [1,0], [2,0], [2,1], [2,2]]),
	np.array([[0,0], [0,1], [0,2], [0,3]]),
	np.array([[0,0], [1,0], [0,1], [1,1]])
)

def main():
	# 1
	falling_rocks(2022)

	# 2
	# The number of different blocks and the number of jets are both prime numbers,
	# so the smallest pattern they'll produce is the size of their product.
	smallest_repeating_sequence = len(jets) * len(shapes)

	# This took a long time but still didn't find any pattern.
	pattern_search(smallest_repeating_sequence * 150)

def falling_rocks(rock_count:int) -> list[int]:
	jet = cycle(jets)
	shape = cycle(shapes)
	tower = set(((0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)))
	tallest = 0
	height_changes = []

	def intersects_wall(block:NDArray) -> bool:
		return block[0,0] == -1 or block[-1,0] == 7

	def intersects_tower(block:NDArray) -> bool:
		shared_blocks = set(map(tuple, block)) & tower
		return len(shared_blocks) > 0

	down = np.array([0,-1])

	for i in range(rock_count):
		if i % 1000 == 0:
			# Track progress and prune tower data.
			if i % 10_000 == 0: print(i)
			tower = {n for n in tower if n[1] > tallest - 100}

		block = next(shape).copy()
		block += [2, tallest + 1]

		# The first three jet pushes are too high to hit the tower.
		for _ in range(3):
			movement = block + next(jet)
			if not intersects_wall(movement):
				block = movement

		while True:
			movement = block + next(jet)
			if not (intersects_wall(movement) or intersects_tower(movement)):
				block = movement

			movement = block + down
			if not intersects_tower(movement):
				block = movement
				continue

			# Block landed
			old_tall = tallest
			tallest = max(tallest, max(block[:,1]))
			height_changes.append(tallest - old_tall)

			tower |= set(map(tuple, block))
			break

	print(tallest)
	return height_changes

def pattern_search(rock_count:int):
	try:
		changes = np.load(cache)
	except FileNotFoundError:
		changes = np.array([])

	if len(changes) < rock_count:
		changes = np.array(falling_rocks(rock_count))
		np.save(cache, changes)
		return

	min_repeat = len(jets) * len(shapes)
	for stacks in range(1, rock_count // (2 * min_repeat)):
		print(f"\n{stacks = }\n")
		sequence_size = stacks * min_repeat

		for start in range(rock_count - 2 * sequence_size):
			if start % 50_000 == 0:
				print(start)

			# Check if two subsequent sequences match.
			nextrep = start + sequence_size
			if not (
					all(changes[start:start + 64] == changes[nextrep:nextrep + 64]) and
					all(changes[start:start + sequence_size] == changes[nextrep:nextrep + sequence_size])):
				continue

			# Check if all sequences in the examined data match.
			n = (rock_count - start) // sequence_size
			test = changes[start:start + n * sequence_size].reshape((n, sequence_size))
			match = test == test[0]
			if np.all(match) and n > 1:
				print(
					"\n",
					f"{stacks = }",
					f"{start = }",
					f"{sequence_size = }",
					f"matched sequences = {n}",
					sep="\n")
				return

if __name__ == "__main__":
	print()
	main()
