import numpy as np
import pygame as pg
from itertools import cycle
from math import sqrt

from typing import Iterable, overload
from pygame import SurfaceType

with open("17.txt", "r", newline="\n") as f:
	jets = [1 if char == ">" else -1 for char in f.read().strip()]
# jets = [1 if char == ">" else -1 for char in ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]

shapes = (
	np.array([[0,0], [1,0], [2,0], [3,0]]),
	np.array([[1,0], [0,1], [1,1], [2,1], [1,2]]),
	np.array([[0,0], [1,0], [2,0], [2,1], [2,2]]),
	np.array([[0,0], [0,1], [0,2], [0,3]]),
	np.array([[0,0], [1,0], [0,1], [1,1]])
)

SCALE = 10
SCREEN_HEIGHT = 100
GOLD_RAT = (1 + sqrt(5)) / 2

def main():
	window = make_gameparts("tetris", (SCALE * 7, SCALE * SCREEN_HEIGHT))
	resting_rocks = pg.Surface((7, SCREEN_HEIGHT)); resting_rocks.fill((255,255,255))
	falling_rocks = pg.Surface((7, SCREEN_HEIGHT), flags=pg.SRCALPHA); falling_rocks.fill((0,0,0,0))

	def draw(*surfaces:SurfaceType) -> None:
		window.fill((200,200,200))
		for s in surfaces:
			window.blit(s, (0,0))
		pg.display.update()

	tower = np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0]])

	black = np.broadcast_to([0], (7,3))
	tower = np.append(tower, black, axis=1)

	block_color = [0, 60, 60]

	draw(paint_blocks(resting_rocks, tower, (255,255,255)))
	while not pg.key.get_pressed()[pg.K_SPACE]:
		pg.event.pump()

	jet = cycle(jets)
	shape = cycle(shapes)
	for i in range(1_000_000):
		block = next(shape).copy()
		block += [2, max(tower[:,1]) + 4]

		block_color[0] = round(360 * i * GOLD_RAT)
		block = np.append(block, np.broadcast_to(block_color, (len(block), len(block_color))), axis=1)

		while True:
			if pg.event.get(eventtype=pg.QUIT) or pg.key.get_pressed()[pg.K_ESCAPE]:
				pg.quit()
				return
			pg.event.pump()
			draw(
				paint_blocks(resting_rocks, tower, background=(255,255,255)),
				paint_blocks(falling_rocks, block))
			pg.time.delay(25)

			movement = block.copy(); movement[:,0] += next(jet)
			can_move = (
				not any(movement[:,0] == -1) and
				not any(movement[:,0] == 7) and
				not anyin(movement[:,0:2], tower[:,0:2])
			)
			if can_move:
				block = movement

			movement = block.copy(); movement[:,1] += -1
			if not anyin(movement[:,0:2], tower[:,0:2]):
				block = movement
			else:
				tower = np.concatenate((tower, block))
				break

		if max(tower[:,1]) >= 95:
			tower[:,1] -= 60
			subterr = tower[:,1] < 0
			tower = tower[~subterr]

			tower = tower[:,0:3]
			block_color = [0]

def paint_blocks(surface:SurfaceType, coords, background=(0,0,0,0)) -> SurfaceType:
	surface.fill(background)
	for x, y, *hue in coords:
		surface.set_at((x, SCREEN_HEIGHT - 1 - y), hsv_to_rgb(*hue))

	return pg.transform.scale_by(surface, SCALE)

def hsv_to_rgb(h:int, s:int=60, v:int=60) -> list[int]:
	def hue_trapezoid(degree:int) -> float:
		sawtooth = abs((degree % 360) - 180) / 60 - 1
		return clamp(sawtooth, 0, 1)

	normrgb = (
		v / 100 * (s / 100 * (hue_trapezoid(h - corner) - 1) + 1)
		for corner in (0, 120, 240)
	)
	return [round(255 * channel) for channel in normrgb]

def anyin(a, b) -> bool:
	for x in a:
		eq = x == b
		if any(np.all(eq, axis=1)):
			return True
	return False

@overload
def clamp(x:int, low:int, high:int) -> int: ...
@overload
def clamp(x:float, low:float, high:float) -> float: ...

def clamp(x, low, high):
	return max(min(high, x), low)

def make_gameparts(title="Pygame window", window_size=(800,600)) -> SurfaceType:
	pg.init()
	pg.display.set_caption(title)
	pg.event.set_blocked(None)
	pg.event.set_allowed(pg.QUIT)
	pg.event.set_allowed(pg.KEYDOWN)
	window = pg.display.set_mode(window_size)
	return window

if __name__ == "__main__":
	print()
	main()
