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
	pattern_search(100_000)

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

	changes = changes[:rock_count]

	for size in range(2, rock_count // 2):
		# Check if the last two subsequent sequences match.
		prel_top = -size + 64 if -size + 64 < 0 else rock_count
		if not (
				all(changes[-size : prel_top] == changes[-2 * size : prel_top - size]) and
				all(changes[-size: ] == changes[-2 * size : -size])):
			continue

		# Count how many subsequent sequences match and where they first start matching.
		n = rock_count // size
		test = changes[-n * size:].reshape((n, size))
		matching = np.all(test == test[-1], axis=1)
		last_nonmatch = np.flatnonzero(matching == False)[-1]
		matching_count = len(matching) - last_nonmatch - 1
		start = rock_count % size + last_nonmatch * size + 1

		if matching_count > 2:
			print(
				f"{size = }",
				f"{start = }",
				f"{matching_count = }",
				sep="\n", end="\n\n")
			break

	first_bit = 10**12 % size
	while start > first_bit:
		first_bit += size

	# Convert to python ints since numpy ints can overflow.
	begining_height = int(sum(changes[:first_bit]))
	repeating_height = int(sum(changes[first_bit:first_bit + size]))
	repeat_count = (10**12 - first_bit) // size
	print(
		f"{first_bit = }",
		f"{begining_height = }",
		f"{repeating_height = }",
		f"{repeat_count = }",
		sep="\n", end="\n\n")

	total_height = begining_height + repeating_height * repeat_count
	print(total_height)

if __name__ == "__main__":
	print()
	main()
