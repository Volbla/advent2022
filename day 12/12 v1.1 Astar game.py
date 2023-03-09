import numpy as np
import pygame as pg
from math import inf
from collections import deque

# /// TYPING SHIT ///

from typing import Callable, Sequence, overload, Any
from nptyping import NDArray, Int, Bool

# Subsequences contain parallel y- and x-coordinates.
# Compatible with numpy simultaneous indexing.
onecoord = tuple[int,...] | NDArray[Any, Int]
Indices = tuple[onecoord, onecoord]

# Compatible with regular iteration over individual points.
Point = tuple[int, int]
Coordinates = Sequence[Point]

BoolMask = NDArray[Any, Bool]

@overload
def transpose(tuptup:Indices) -> Coordinates: ...
@overload
def transpose(tuptup:Coordinates) -> Indices: ...

# /// END TYPING SHIT ///

def transpose(tuptup):
	# Transforms between the two coordinate types.
	return tuple(zip(*tuptup))

SCALE = 8

with open("12.txt", "r", newline="\n", encoding="ascii") as f:
	heightmap = np.array([[ord(c) for c in s] for s in f.read().splitlines()])

start:Point = transpose(np.nonzero(heightmap == ord("S")))[0]
end:Point = transpose(np.nonzero(heightmap == ord("E")))[0]
heightmap[start] = ord("a")
heightmap[end] = ord("z")


def main():
	def lower_estimate(p:Point) -> int:
		# Straight manhattan distance.
		return abs(end[0] - p[0]) + abs(end[1] - p[1])

	y, x = heightmap.shape

	window = make_gameparts("A* animation", (SCALE * x, SCALE * y))
	background = pg.image.load("map_small.png")
	big_background = pg.transform.scale_by(background, SCALE)
	window.blit(big_background, (0,0))
	pg.display.update()

	draw_surface = pg.Surface((x, y), flags=pg.SRCALPHA)
	draw_surface.fill((0,0,0,0))

	# Start paused.
	while True:
		event = pg.event.wait()
		if pg.key.get_pressed()[pg.K_SPACE]: break

	path = A_Star(start, end, lower_estimate, window, draw_surface, big_background)

	if path is None:
		print("End was unreachable")
		return

	while True:
		event = pg.event.wait()
		if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE] or pg.key.get_pressed()[pg.K_SPACE]:
			break

	pg.quit()
	return


def A_Star(start:Point, goal:Point, h:Callable, window, draw_surface, background) -> Coordinates|None:
	openSet:set[Point] = {start,}

	cameFrom:dict[Point, Point] = {}

	gScore:dict[Point, int] = {}
	gScore[start] = 0

	fScore:dict[Point, int] = {}
	fScore[start] = h(start)

	snakesize = 30
	snakequeue = deque(maxlen=snakesize)
	snakequeue.append(tuple(reversed(start)))

	while openSet:
		current = min(openSet, key=fScore.get)
		if current == goal:
			return reconstruct_path(cameFrom, current)

		# /// PYGAME
		snakequeue.append(tuple(reversed(current)))
		for i, pix in enumerate(snakequeue):
			realalpha = (i / (snakesize - 1)) ** (2.2)
			draw_surface.set_at(pix, (0, 200, 0, 255 * realalpha))

		window.blit(background, (0,0))
		window.blit(pg.transform.scale_by(draw_surface, SCALE), (0,0))
		pg.display.update()
		pg.event.clear()
		pg.time.delay(3)

		if pg.key.get_pressed()[pg.K_ESCAPE]: return
		# /// END PYGAME

		openSet.remove(current)
		for neighbor in walkable_from(current):
			tentative_gScore = gScore[current] + 1

			if tentative_gScore < gScore.get(neighbor, inf):
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore
				fScore[neighbor] = tentative_gScore + h(neighbor)

				if neighbor not in openSet:
					openSet.add(neighbor)

	return None


def walkable_from(pos:Point) -> Coordinates:
	y, x = neighbors(pos)
	slope_mask = heightmap[(y,x)] - heightmap[pos] <= 1
	walkable = (y[slope_mask], x[slope_mask])
	return transpose(walkable)


def neighbors(pos:Point) -> Indices:
	ymax, xmax = heightmap.shape
	edge_mask = np.array([
		pos[0] != 0,
		pos[0] != ymax - 1,
		pos[1] != 0,
		pos[1] != xmax - 1
		], dtype=bool
	).squeeze()

	# up, down, left, right
	ydir = np.array([-1,1,0,0])
	xdir = np.array([0,0,-1,1])

	available_slots = (pos[0] + ydir[edge_mask], pos[1] + xdir[edge_mask])
	return available_slots


def reconstruct_path(cameFrom:dict[Point, Point], current:Point) -> Coordinates:
	total_path = [current]

	while current in cameFrom.keys():
		current = cameFrom[current]
		total_path.append(current)

	total_path.reverse()
	return total_path


def make_gameparts(title="Pygame window", window_size=(800,600)):
	pg.init()
	pg.display.set_caption(title)
	window = pg.display.set_mode(window_size)

	# We only need mouse movement if button is held down.
	pg.event.set_blocked(pg.MOUSEMOTION)
	# Clear any events queued by the setup.
	pg.event.clear()

	return window


if __name__ == "__main__":
	print()
	main()
