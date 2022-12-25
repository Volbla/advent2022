import re
from operator import itemgetter
import numpy as np

with open("15.txt", "r", newline="\n") as f:
	inptext = f.read().splitlines()

def coordmatch(prefix:str) -> list:
	pattern = re.compile(f"{prefix} ?x=(-?\d+), y=(-?\d+)")
	return [tuple(map(int, pattern.search(line).groups())) for line in inptext]

sensors = coordmatch("Sensor at")
beacons = coordmatch("beacon is at")

radii = [
	abs(sen[0] - beac[0]) + abs(sen[1] - beac[1])
	for sen, beac in zip(sensors, beacons)
]

def main():
	# 1
	part1()

	# 2
	x, y = part2()
	print(x * 4_000_000 + y)

	# 2.2
	for i in range(10):
		result = part2vec(400_000, i)
		if result is not None:
			x, o = result
			y = 400_000 * i + o
	print(int(x) * 4_000_000 + y)

def part1():
	seg = [
		(s[0] - t, s[0] + t)
		for s, r in zip(sensors, radii)
		if (t := r - abs(2_000_000 - s[1])) >= 0
	]
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

	return covered_distance

def part2(limit):
	x_interval = (0,0)
	for i in range(limit + 1):
		# Track progress
		if i % 100_000 == 0:
			print(i)

		if (hole := part2_loop(i)) is not None:
			x_interval = hole
			y = i
			# break if confident

	if x_interval[1] - x_interval[0] != 2:
		print("Hole too big")
		return

	x = sum(x_interval) // 2
	return x, y

def part2_loop(row):
	# covered segments
	seg = [
		(s[0] - t, s[0] + t)
		for s, r in zip(sensors, radii)
		if (t := r - abs(row - s[1])) >= 0
	]
	seg.sort(key=itemgetter(0))

	high = seg[0][1]
	for nextseg in seg[1:]:
		if high < nextseg[0] - 1 and high <= 4_000_000 and nextseg[0] >= 0:
			return (high, nextseg[0])
		high = max(high, nextseg[1])

	return None

def part2vec(batch_size, iteration):
	# Vectorizing is fun yet painful. This seems about
	# twice as fast as the loop. Have to batch the calls though,
	# or it consumes all my memory.

	snump = np.array(sensors)
	rnump = np.array(radii)

	def f(row, s_i, side):
		thickness = rnump[s_i] - abs(row + (batch_size * iteration) - snump[s_i, 1])
		sign = 2 * side - 1
		return (snump[s_i, 0] + sign * thickness) * (thickness >= 0)

	rowtouch = np.fromfunction(f, (batch_size, len(sensors), 2), dtype=np.int32)
	order = np.argsort(rowtouch, axis=1)
	order[..., 1] = order[..., 0]

	ordered = np.take_along_axis(rowtouch, order, axis=1)
	x_overlap = np.maximum.accumulate(ordered, axis=1)
	difference = x_overlap[:, :-1, 1] - x_overlap[:, 1:, 0]

	if np.any(hole := (difference < 0)):
		i = np.nonzero(hole) + (1,)
		return ordered[i][0], i[0][0]

	return None

def curiosity():
	from time import perf_counter as p
	start = p()

	# This is how i originally built the list of sensor coverage.
	for _ in range(50_000):
		seg = []
		for s, r in zip(sensors, radii):
			dist = abs(2_000_000 - s[1])
			if (thickness := r - dist) >= 0:
				seg.append((s[0] - thickness, s[0] + thickness))
	print(f"Looping: {p() - start}"); start = p()

	# When tweaking i discovered that a comprehension with extra
	# generators (for readability/simplicity) is slower than looping.
	for _ in range(50_000):
		thickness = (r - abs(2_000_000 - s[1]) for s, r in zip(sensors, radii))
		seg = [(s[0] - t, s[0] + t) for s, t in zip(sensors, thickness) if t >= 0]
	print(f"Extra generator: {p() - start}"); start = p()

	# But walrus assginment makes it writable in a single comprehension.
	# It's only slightly faster than looping though.
	for _ in range(50_000):
		seg = [
			(s[0] - t, s[0] + t)
			for s, r in zip(sensors, radii)
			if (t := r - abs(2_000_000 - s[1])) >= 0
		]
	print(f"One comprehension: {p() - start}")

if __name__ == "__main__":
	print()
	main()
