import numpy as np
from itertools import product
from math import inf

site_example = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".splitlines()

with open("18.txt", "r", newline="\n") as f:
	inptext = f.read().splitlines()
cube_coords = [tuple(map(int, line.split(","))) for line in inptext]
unit_cubes = np.zeros((23,23,23), dtype=bool)
unit_cubes[tuple(zip(*cube_coords))] = True

# 1
faces = [
	np.roll(unit_cubes, sign, axis=axis)
	& ~unit_cubes
	for axis, sign in product(range(3), (-1,1))
]
print(np.count_nonzero(faces))

# for 2
drop = set(cube_coords)
everyone = {(a, b, c) for a, b, c in product(range(0, 23), repeat=3)}

def tupadd(tup, index, value):
	"""Handling immutability."""
	a = list(tup)
	a[index] += value
	return tuple(a)

friends = {
	coord: [n for n in (tupadd(coord, axis, sign)
	for axis, sign in product(range(3), (-1,1)))
	if n in everyone]
	for coord in everyone
}

def walkable_from(coord):
	return (x for x in friends[coord] if x not in drop)

def flood_fill(start):
	openSet = {start,}

	cameFrom = {}

	gScore = {}
	gScore[start] = 0

	while openSet:
		current = sorted(list(openSet), key=lambda x: gScore[x])[0]

		openSet.remove(current)
		for neighbor in walkable_from(current):
			tentative_gScore = gScore[current] + 1

			if tentative_gScore < gScore.get(neighbor, inf):
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore

				if neighbor not in openSet:
					openSet.add(neighbor)

	return cameFrom

# 2
outside = flood_fill((0,0,0))
outside_mask = np.zeros((23,23,23), dtype=bool)
outside_mask[tuple(zip(*outside.keys()))] = True

wet = [f & outside_mask for f in faces]
print(np.count_nonzero(wet))
