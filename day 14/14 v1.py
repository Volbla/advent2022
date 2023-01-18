import numpy as np
from PIL import Image

with open("14.txt", "r", newline="\n") as f:
	inptext:list[str] = f.read().splitlines()

def main():
	room = rock_drawing()
	draw_mask(room)

	# 1
	filled_room = counting(room)
	just_sand = filled_room != room
	print(np.count_nonzero(just_sand))
	draw_mask(filled_room)

	# 2
	# Expand to the side
	height, width = room.shape
	long_room = np.concatenate((room, np.zeros((height, height), dtype=bool)), axis=1)
	# Add floor
	floor_room = np.concatenate((long_room, long_room[-2:,:]), axis=0)
	floor_room[-2,:] = False
	floor_room[-1,:] = True

	filled_room = counting(floor_room, True)
	just_sand = filled_room != floor_room
	print(np.count_nonzero(just_sand))
	draw_mask(filled_room)

def counting(room, has_floor=False):
	# Storing sand index as plain variables. Much fast.

	sandy_room = room.copy()
	height = room.shape[0]

	dist_check = 0 if has_floor else height - 1
	y = dist_check + 1
	while y != dist_check:
		x = 500
		for y in range(height):
			if not sandy_room[y, x]:
				continue

			if not sandy_room[y, x - 1]:
				x -= 1
				continue

			if not sandy_room[y, x + 1]:
				x += 1
				continue

			y -= 1
			sandy_room[y, x] = True
			break

	return sandy_room

def rock_drawing():
	drawn_pixels = ([], [])
	for line in inptext:
		edges = [[int(x) for x in pair.split(",")] for pair in line.split(" -> ")]
		for a, b in zip(edges[:-1], edges[1:]):
			# This axis stays the same
			i = a[1] == b[1]
			# This axis varies, i.e. draws the line
			r = not i

			start = min(a[r], b[r])
			stop = max(a[r], b[r])
			middlepoints = range(start, stop + 1)

			# Reverse the order since numpy arrays are ordered (y, x)
			drawn_pixels[i].extend(list(middlepoints))
			drawn_pixels[r].extend([a[i] for _ in middlepoints])

	shape = (max(drawn_pixels[0]) + 1, max(drawn_pixels[1]) + 3)
	arr = np.zeros(shape, dtype=bool)
	arr[drawn_pixels] = True

	return arr

def draw_mask(mask) -> None:
	greypic = (~mask).astype(np.uint8) * 255

	reachmask = mask[:-1,:] if all(mask[-1,:]) else mask
	xreach = np.flatnonzero(np.any(reachmask, axis=0))
	xmin = min(xreach) - 2
	xmax = max(xreach) + 2

	scaled = np.repeat(greypic[:, xmin:xmax + 1], 5, axis=1)
	scaled = np.repeat(scaled, 5, axis=0)
	Image.fromarray(scaled, mode="L").show()


# Slow attempts.
def counting_arr(room):
	# Storing sand index in an array. Must be converted to tuple to actually index. Medium-fast.

	sandy_room = room.copy()
	height = room.shape[0]

	sand = np.array([0, 500])
	falldown = np.array([1, 0])
	fallleft = np.array([0, -1])
	fallright = np.array([0, 1])

	distance = 0
	while distance != height - 2:
		falling_sand = sand

		for distance in range(height - 1):
			if not sandy_room[tuple(down := falling_sand + falldown)]:
				falling_sand = down

			elif not sandy_room[tuple(left := down + fallleft)]:
				falling_sand = left

			elif not sandy_room[tuple(right := down + fallright)]:
				falling_sand = right
			else:
				sandy_room[tuple(falling_sand)] = True
				break

	return sandy_room

def rolling(room):
	# Rolling a boolean array with one true element. Slow af.

	sandy_room = room.copy()
	height = sandy_room.shape[0]

	sand = np.zeros_like(sandy_room)
	sand[0, 500] = True

	distance = 0
	while distance != height - 1:
		falling_sand = sand.copy()
		for distance in range(height):
			if not np.any(sandy_room & (down := np.roll(falling_sand, 1, axis=0))):
				falling_sand = down

			elif not np.any(sandy_room & (left := np.roll(down, -1, axis=1))):
				falling_sand = left

			elif not np.any(sandy_room & (right := np.roll(down, 1, axis=1))):
				falling_sand = right
			else:
				sandy_room |= falling_sand
				break

	return sandy_room

if __name__ == "__main__":
	print()
	main()
