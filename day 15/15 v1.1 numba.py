import re
from operator import itemgetter
from numba import njit, jit
from numba.typed import List

with open("15.txt", "r", newline="\n") as f:
	inptext = f.read().splitlines()

sensors = List()
beacons = List()
for line in inptext:
	match1 = re.search(r"Sensor at x=(-?\d+), y=(-?\d+)", line)
	sensors.append((int(match1[1]), int(match1[2])))

	match2 = re.search(r"beacon is at x=(-?\d+), y=(-?\d+)", line)
	beacons.append((int(match2[1]), int(match2[2])))

radii = List()
for s, b in zip(sensors, beacons):
	dx = abs(s[0] - b[0])
	dy = abs(s[1] - b[1])
	radius = dx + dy
	radii.append(radius)

# 1
def part1():
	# covered segments
	seg = []
	for s, r in zip(sensors, radii):
		dist = abs(2_000_000 - s[1])
		if (thickness := r - dist) >= 0:
			seg.append((s[0] - thickness, s[0] + thickness))
	seg.sort(key=itemgetter(0))

	meddling_beacons = [b[0] for b in set(beacons) if b[1] == 2_000_000]
	covered_distance = 0
	i = 0
	while i < len(seg):
		low = seg[i][0]
		high = seg[i][1]

		# Merge adjacent segments if they overlap or touch.
		while (i + 1 < len(seg)) and (high >= seg[i + 1][0] - 1):
			high = max(high, seg[i + 1][1])
			i += 1

		covered_distance += high - low + 1
		for b in meddling_beacons:
			if low <= b <= high:
				covered_distance -= 1
		i += 1

	print(covered_distance)

# 2
@njit
def part2_loop(row, sensors, radii):
	# covered segments
	seg = []
	for s, r in zip(sensors, radii):
		dist = abs(row - s[1])
		thickness = r - dist
		if (thickness) >= 0:
			seg.append((s[0] - thickness, s[0] + thickness))
	seg.sort(key=lambda x: x[0])

	high = seg[0][1]
	for a, b in zip(seg[:-1], seg[1:]):
		if high < b[0] - 1 and high <= 4_000_000 and b[0] >= 0:
			return (high + b[0]) // 2
		high = max(high, b[1])

	return -1

def main():
	from time import perf_counter as p

	s = p()
	for i in range(4_000_001):
		if i % 100_000 == 0:
			# Track progress
			print(i, p() - s)
			s = p()

		if (spot := part2_loop(i, sensors, radii)) != -1:
			x = spot
			y = i
			# break if confident

	print(x * 4_000_000 + y)

if __name__ == "__main__":
	print()
	main()
