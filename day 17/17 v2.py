import numpy as np
from itertools import cycle

with open("17.txt", "r", newline="\n") as f:
	jets = [np.array([1,0]) if char == ">" else np.array([-1,0]) for char in f.read().strip()]
# Site example
# jets = [[1,0] if char == ">" else [-1,0] for char in ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]

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

	# 2. Took a long time but still not enough.
	min_man = len(jets) * 5
	pattern_search(min_man * 150)

def falling_rocks(rock_count:int):
	jet = cycle(jets)
	shape = cycle(shapes)
	tower = set(((0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)))
	tallest = 0
	height_change = []
	down = np.array([0,-1])

	for i in range(rock_count):
		if i % 1000 == 0:
			# print(i)
			tower = {n for n in tower if n[1] > tallest - 100}
		block = next(shape).copy()
		block += [2, tallest + 1]

		for _ in range(3):
			push = next(jet)
			if (push[0] == -1 and block[0,0] != 0) or (push[0] == 1 and block[-1,0] != 6):
				block += push

		while True:
			push = next(jet)
			if (push[0] == -1 and block[0,0] != 0) or (push[0] == 1 and block[-1,0] != 6):
				movement = block + push
				if not set(map(tuple, movement)) & tower:
					block = movement

			movement = block + down
			if not set(map(tuple, movement)) & tower:
				block = movement
				continue

			# Block landed
			old_tall = tallest
			tallest = max(tallest, max(block[:,1]))
			height_change.append(tallest - old_tall)

			tower |= set(map(tuple, block))
			break

	print(tallest)
	return height_change

def pattern_search(rock_count:int):
	try:
		changes = np.load("fromdata.npy")
	except FileNotFoundError:
		changes = np.array([])

	if len(changes) < rock_count:
		changes = np.array(falling_rocks(rock_count))
		np.save("fromdata.npy", changes)
		return

	min_repeat = len(jets) * 5
	done = False
	for stack in range(1, rock_count // (2 * min_repeat)):
		print("\n ", stack)
		rep = stack * min_repeat

		for i in range(rock_count - 2 * rep):
			if i % 10_000 == 0:
				print(i)

			nextrep = i + rep
			if not (
				all(changes[i:i + 64] == changes[nextrep:nextrep + 64]) and
				all(changes[i:i + rep] == changes[nextrep:nextrep + rep])):
				continue

			n = (rock_count - i) // rep
			test = changes[i:i + n * rep].reshape((n, rep))
			same = test == test[0]
			if np.all(same) and n > 1:
				print("\n\n", stack, i, n * rep, test.shape)
				done = True
				break

		if done:
			break

if __name__ == "__main__":
	print()
	main()
