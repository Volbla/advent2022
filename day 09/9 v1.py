import numpy as np

with open("9.txt", "r", newline="\n") as f:
	inp = f.read().splitlines()
commands = [(s[0], int(s[2:])) for s in inp]

def ropedrag(knots:int) -> int:
	steps = np.array([[1,0], [0,1], [-1,0], [0,-1]])

	rope = np.tile([0,0], [knots,1])
	visitations = set()
	visitations.add(tuple(rope[-1]))

	for c in commands:
		walk = (
			steps[0] if c[0] == "R" else
			steps[1] if c[0] == "U" else
			steps[2] if c[0] == "L" else
			steps[3] #if c[0] == "D"
		)
		for _ in range(c[1]):
			rope[0] += walk

			for i in range(1,knots):
				offset = rope[i-1] - rope[i]

				if any(np.abs(offset) > 1):
					rope[i] += np.sign(offset)
				else:
					break

			visitations.add(tuple(rope[-1]))

	return len(visitations)

from volbla import mytiming
one = mytiming.standard(ropedrag, 2)
two = mytiming.standard(ropedrag, 10)
print(two)
