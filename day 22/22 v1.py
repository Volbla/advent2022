import re
import numpy as np
from numpy import array
from itertools import cycle

from typing import Sequence
from nptyping import NDArray, Bool, Shape
BoolSquare = NDArray[Shape["Dim,Dim"], Bool]

with open("22.txt", "r", newline="\n") as f:
	inptext = f.read()
example = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

inp1, inp2 = inptext.split("\n\n")
DRAW:bool = False

def main():
	instructions = [int(x) if x.isnumeric() else x for x in re.findall(r"\d+|L|R", inp2)]

	crooked_board = inp1.splitlines()
	width = max(map(len, crooked_board))
	board = [s.ljust(width) for s in crooked_board]

	# 1
	calculate_points(*traverse_flat_map(board, instructions))


def traverse_flat_map(board, instructions):
	transpose_board = ["".join(line[i] for line in board) for i in range(len(board[0]))]

	def tiles(s:str) -> tuple[int,int]:
		return re.search(r"[^ ]+", s).span()
	rows = list(map(tiles, board))
	columns = list(map(tiles, transpose_board))

	def obstacles(s:str):
		return array(list(map(re.Match.start, re.finditer(r"#", s))))
	row_blocks = list(map(obstacles, board))
	column_blocks = list(map(obstacles, transpose_board))

	tile_axis = (rows, columns)
	block_axis = (row_blocks, column_blocks)

	position = array([rows[0][0], 0])
	direction = array([1,0])
	# Rotation matrices
	rotation = {"R": array([[0,-1], [1,0]]), "L": array([[0,1], [-1,0]])}

	if DRAW:
		window = painter(board, transpose_board, rows, position)

	for inst in instructions:
		if isinstance(inst, str):
			direction = rotation[inst] @ direction
			continue

		if DRAW:
			window.sprites[0].move_to(tuple(position))
			if not window.rendering(500): return

		i = np.flatnonzero(direction)[0]
		move, stay = position[i], position[1 - i]

		sign = direction[i]
		axis = tile_axis[i][stay]
		length = axis[1] - axis[0]

		blocks = block_axis[i][stay]
		if len(blocks) == 0:
			position[i] = (move + sign * inst) % length + axis[0]
			continue

		block_distances = (blocks - move) % length
		distance_limit = (
			min(block_distances) - 1
			if sign == 1 else
			abs(max(block_distances - length)) - 1
		)
		dist = min(distance_limit, inst)
		position[i] = (move - axis[0] + sign * dist) % length + axis[0]

	return position, direction


def painter(board, transpose_board, rows, position):
	# Simple visualization

	from volbla.gaming.PixelPainter import GameWindow
	window = GameWindow("day 22", (len(transpose_board), len(board)), 5)

	for y, row in enumerate(rows):
		line = [[x, y] for x in range(*row)]
		stripe_col = 240,60,100 - 20 * (y % 2 == 0)
		window.backgrounds[0].draw_pixels(
			line, stripe_col)

	block_array = array(list(map(list, transpose_board))) == "#"
	window.backgrounds[0].draw_pixels(
		tuple(zip(*np.nonzero(block_array))),
		(0,0,0))

	window.add_sprite((1,1), (255,100,100), tuple(position))
	# window.stand_by(10)
	# window.frame_stepping()

	return window

def calculate_points(position, direction):
	dx, dy = direction
	dpoints = (
		0 if dx == 1 else
		1 if dy == 1 else
		2 if dx == -1 else
		3 #if dy == -1
	)
	position += 1
	print(1000 * position[1] + 4 * position[0] + dpoints)

if __name__ == "__main__":
	print()
	main()
