import numpy as np
from PIL import Image
from itertools import count, pairwise

with open("14.txt", "r", newline="\n") as f:
	inptext:list[str] = f.read().splitlines()

def main():
	room = rock_drawing()

	# 1
	filled_room = counting(room)
	just_sand = filled_room - room
	print(len(just_sand))

	# 2
	filled_room = counting(room, max(pix[1] for pix in room) + 2)
	just_sand = filled_room - room
	print(len(just_sand))

def counting(room:set, floor=None):
	sandy_room = room.copy()
	height = floor + 1 if floor else max(pix[1] for pix in room) + 1

	dist_check = 0 if floor else height - 1
	y = dist_check + 1
	while y != dist_check:
		x = 500
		for y in range(height):
			if floor and y == floor:
				sandy_room.add((x, y - 1))
				break

			if (x, y) not in sandy_room:
				continue

			if (x - 1, y) not in sandy_room:
				x -= 1
				continue

			if (x + 1, y) not in sandy_room:
				x += 1
				continue

			y -= 1
			sandy_room.add((x, y))
			break

	return sandy_room

def rock_drawing() -> set:
	drawn_pixels = set()

	for line in inptext:
		edges = (tuple(map(int, pair.split(","))) for pair in line.split(" -> "))
		for a, b in pairwise(edges):
			# This axis stays the same
			i = a[1] == b[1]
			# This axis varies, i.e. draws the line
			r = not i

			start = min(a[r], b[r])
			stop = max(a[r], b[r])

			drawn_pixels |= {
				(a[i], x) if i == 0 else (x, a[i])
				for x in range(start, stop + 1)
			}

	return drawn_pixels

if __name__ == "__main__":
	print()
	main()
