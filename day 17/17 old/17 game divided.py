import numpy as np
import pygame as pg
from itertools import cycle, count
from math import sqrt
from functools import partial

from typing import Iterable, overload, Sequence, Any
from pygame import SurfaceType
from nptyping import NDArray, Bool, Shape

with open("17.txt", "r", newline="\n") as f:
	jets = [[1,0] if char == ">" else [-1,0] for char in f.read().strip()]
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
	backgrounds = [surface_1.copy() for _ in range(SECTIONS)]
	bigbackgrounds = list(map(stretch, backgrounds))
	sprite = pg.Surface((4, 4), flags=pg.SRCALPHA)

	# Iterators
	jet = cycle(jets)
	shape = cycle(shapes)
	hue = (round(360 * i * GOLD_RAT) for i in count(1))
	next_section = 1

	tower = np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0]])
	bigbackgrounds[0] = draw_pixels(backgrounds[0], tower, (0,0,0), (255,255,255))

	block = next(shape).copy()
	bigsprite = draw_pixels(sprite, block, [next(hue)])
	block += [2, max(tower[:,1]) + 4]

	# Starting paused
	# while not pg.key.get_pressed()[pg.K_SPACE]:
	# 	pg.event.pump()

	while drawing(window, bigbackgrounds, bigsprite, block):
		movement = block + next(jet)
		is_blocked = (
			any(movement[:,0] == -1) or
			any(movement[:,0] == 7) or
			anyin(movement, tower)
		)
		if not is_blocked:
			block = movement

		movement = block + [0,-1]

		if not anyin(movement, tower):
			block = movement
			continue

		# Block landed
		tower = np.concatenate((tower, block))
		bigbackgrounds = stamp_background(backgrounds, sprite, block)

		block = next(shape).copy()
		bigsprite = draw_pixels(sprite, block, [next(hue)])
		block += [2, max(tower[:,1]) + 4]

		if max(block[:,1]) >= next_section * HEIGHT:
			i = next_section % SECTIONS
			backgrounds[i].fill((255,255,255))
			mask = section_masks(tower[:,1])[i]
			tower = tower[~mask]
			next_section += 1

class ScaledSurface:
	def __init__(self, shape, color, scale, flags=0):
		self.small = pg.Surface(shape, flags)
		self.small.fill(color)
		self.scale = scale
		self._stretch()

	def _stretch(self):
		self.big = pg.transform.scale_by(self.small, self.scale)

	def fill(self, color):
		self.small.fill(color)
		self.big.fill(color)

	def set_at(self, pixel, color):
		self.small.set_at(pixel, color)

	def blit(self, source, pos):
		if isinstance(source, ScaledSurface):
			self.small.blit(source.small, pos)
			self.big.blit(source.big, pos)
		else:
			self.small.blit(source, pos)
			self._stretch()
		pass

def drawing(window, backgrounds, sprite, pixels):
	wait = 20
	if pg.event.get(eventtype=pg.QUIT) or pg.key.get_pressed()[pg.K_ESCAPE]:
		return False
	if pg.key.get_pressed()[pg.K_SPACE]:
		wait = 300
	pg.event.pump()

	for surf, x in zip(backgrounds, count(0, 8 * SCALE)):
		window.blit(surf, (x, 0))

	x, y = np.amin(pixels, axis=0)
	x1 = (x + 8 * section_from_height(y)) * SCALE
	y1 = (flip(y) - 3) * SCALE

	x2 = (x + 8 * section_from_height(y, 1)) * SCALE
	y2 = (flip(y) - 3 + HEIGHT) * SCALE

	window.blits((
		(sprite, (x1, y1)),
		(sprite, (x2, y2)),
	))

	pg.display.update()
	pg.time.delay(wait)
	return True

def stamp_background(backgrounds, sprite, pixels):
	x, y = np.amin(pixels, axis=0)
	i1 = section_from_height(y)
	i2 = section_from_height(y, 1)

	backgrounds[i1].blit(sprite, (x, flip(y) - 3))
	backgrounds[i2].blit(sprite, (x, flip(y) - 3 + HEIGHT))

	return list(map(stretch, backgrounds))

def draw_pixels(surface, pixels, hsv, fillcolor=(0,0,0,0)):
	surface.fill(fillcolor)
	for x, y in pixels:
		surface.set_at((x, flip(y, surface.get_height())), hsv_to_rgb(*hsv))
	return stretch(surface)

def hsv_to_rgb(h:int, s:int=60, v:int=60) -> list[int]:
	def hue_trapezoid(degree:int) -> float:
		sawtooth = abs((degree % 360) - 180) / 60 - 1
		return clamp(sawtooth, 0, 1)

	normrgb = (
		v / 100 * (s / 100 * (hue_trapezoid(h - corner) - 1) + 1)
		for corner in (0, 120, 240)
	)
	return [round(255 * channel) for channel in normrgb]

def stretch(surface):
	return pg.transform.scale_by(surface, SCALE)

def flip(y, height=HEIGHT):
	return height - 1 - (y % height)

def section_from_height(y, extra_step=0):
	return (y // HEIGHT + extra_step) % SECTIONS

def section_masks(y_coordinates):
	wrapped = y_coordinates % (HEIGHT * SECTIONS)
	borders = np.arange(SECTIONS).reshape((SECTIONS,1)) * HEIGHT
	return np.logical_and(borders <= wrapped, wrapped < borders + HEIGHT)

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
	pg.quit()
