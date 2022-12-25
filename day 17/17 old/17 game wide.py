import numpy as np
import pygame as pg
from itertools import cycle, count
from math import sqrt

from typing import Iterable, overload, Sequence
from pygame import SurfaceType
from nptyping import NDArray, Bool, Shape

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

SECTIONS = 4
WIDTH = (7 + 1) * SECTIONS - 1
HEIGHT = 60
SCALE = 10
GOLD_RAT = (1 + sqrt(5)) / 2

def main():
	window = make_gameparts("tetris", (SCALE * WIDTH, SCALE * HEIGHT))
	window.fill((200,200,200))
	surface_1 = pg.Surface((7, HEIGHT)); surface_1.fill((255,255,255))
	rock_surfs = [surface_1.copy() for _ in range(SECTIONS)]
	for i, surf in enumerate(rock_surfs):
		window.blit(pg.transform.scale_by(surf, SCALE), (8 * i * SCALE, 0))

	# Start paused
	draw(window, tower, (255,255,255), rock_surfs)
	while not pg.key.get_pressed()[pg.K_SPACE]:
		pg.event.pump()

	tower = np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0]])
	# Adding space for color information.
	black = np.broadcast_to([0], (7,3))
	tower = np.append(tower, black, axis=1)
	block_color = [0, 60, 60]

	# Iterators
	jet = cycle(jets)
	shape = cycle(shapes)
	next_section = 1
	for i in range(1_000_000):
		block = next(shape).copy()
		block += [2, max(tower[:,1]) + 4]

		if max(block[:,1]) >= next_section * HEIGHT:
			mask = screen_section_mask(tower[:,1])[next_section % SECTIONS]
			tower = tower[~mask]
			next_section += 1

		color_shape = (len(block), len(block_color))
		block_color[0] = round(360 * i * GOLD_RAT)
		block = np.append(block, np.broadcast_to(block_color, color_shape), axis=1)

		while True:
			# Game stuff
			if pg.event.get(eventtype=pg.QUIT) or pg.key.get_pressed()[pg.K_ESCAPE]:
				pg.quit()
				return
			pg.event.pump()
			to_draw = np.concatenate((tower, block))
			draw(window, to_draw, (255,255,255), rock_surfs)
			pg.time.delay(10)

			# Logic stuff
			movement = block.copy()
			movement[:,0] += next(jet)
			is_blocked = (
				any(movement[:,0] == -1) or
				any(movement[:,0] == 7) or
				anyin(movement[:,0:2], tower[:,0:2])
			)
			if not is_blocked:
				block = movement

			movement = block.copy()
			movement[:,1] += -1

			if not anyin(movement[:,0:2], tower[:,0:2]):
				block = movement
			else:
				tower = np.concatenate((tower, block))
				break

		if next_section - 1 == SECTIONS:
			# When the black color of the floor is gone,
			# we don't need to store saturation and value anymore.
			tower = tower[:,:3]
			block_color = [0]

def draw(window:SurfaceType, pixels, fill_color:Sequence[int], surfaces:list[SurfaceType]) -> None:
	# One mask for each section. Only update the sections with moving blocks.
	in_section = screen_section_mask(pixels[:,1])
	needs_update = np.any(screen_section_mask(pixels[-5:,1]), axis=1)

	for i in np.flatnonzero(needs_update):
		s = surfaces[i]
		s.fill(fill_color)

		for x, y, *hsv in pixels[in_section[i]]:
			s.set_at((x, HEIGHT - 1 - (y % HEIGHT)), hsv_to_rgb(*hsv))

		window.blit(
			pg.transform.scale_by(s, SCALE),
			(8 * i * SCALE, 0)
		)
	pg.display.update()

def screen_section_mask(heights):
	wrapped = heights % (HEIGHT * SECTIONS)
	borders = np.arange(SECTIONS).reshape((SECTIONS,1)) * HEIGHT
	return np.logical_and(borders <= wrapped, wrapped < borders + HEIGHT)

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
