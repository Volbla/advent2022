"""
Press space to start dropping blocks.
Holding space while running slows the movement down.
Press escape to close window.
"""

import numpy as np
import pygame as pg
from itertools import cycle, count, repeat, chain
from math import sqrt

from typing import Sequence
from pygame import SurfaceType
from nptyping import NDArray, Shape, Int, Bool
PixelArray = NDArray[Shape["*,2"], Int] | list[list[int]]

with open("17.txt", "r", newline="\n") as f:
	jets = [[1,0] if char == ">" else [-1,0] for char in f.read().strip()]
# Site example
jets = [[1,0] if char == ">" else [-1,0] for char in ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]

shapes:tuple[PixelArray, ...] = (
	np.array([[0,0], [1,0], [2,0], [3,0]]),
	np.array([[1,0], [0,1], [1,1], [2,1], [1,2]]),
	np.array([[0,0], [1,0], [2,0], [2,1], [2,2]]),
	np.array([[0,0], [0,1], [0,2], [0,3]]),
	np.array([[0,0], [1,0], [0,1], [1,1]])
)

SECTIONS = 25
WIDTH = (7 + 1) * SECTIONS - 1
HEIGHT = 90
SCALE = 8
# For cycling through colors without repeating.
GOLD_RAT = (1 + sqrt(5)) / 2

class ScaledSurface:
	"""Pygame.Surface wrapper containing a scaled up version of the main surface,
	as well as some utilities to keep them synchronized.
	"""

	def __init__(self, shape, color, scale, flags=0):
		self.small = pg.Surface(shape, flags)
		self.small.fill(color)
		self.scale = scale
		self._stretch()

		self.standard = None

	def _stretch(self):
		self.big = pg.transform.scale_by(self.small, self.scale)

	def save(self):
		self.standard = self.small.copy()

	def big_coords(self, x, y):
		"""Returns arguments needed to blit onto a regular (already scaled) pg.Surface."""
		return (self.big, (x * self.scale, y * self.scale))

	def fill(self, color, rect=None):
		if rect is not None:
			self.small.fill(color, rect)
			self.save()
			self._stretch()

		elif self.standard is not None:
			self.small.blit(self.standard, (0,0))
			self._stretch()

		else:
			self.small.fill(color)
			self.big.fill(color)

	def set_at(self, pixel, color):
		"""For now requires manual call to _stretch once finished,
		instead of updating the big surface after each pixel."""
		self.small.set_at(pixel, color)

	def blit(self, source, pos):
		if isinstance(source, ScaledSurface):
			self.small.blit(source.small, pos)
			self.big.blit(*source.big_coords(*pos))
		else:
			self.small.blit(source, pos)
			self._stretch()

	def get_height(self):
		return self.small.get_height()

def main():
	# Pygame objects
	window = make_gameparts("tetris", (WIDTH * SCALE, HEIGHT * SCALE))
	window.fill((200,200,200))
	backgrounds = [ScaledSurface((7, HEIGHT), (255,255,255), SCALE) for _ in range(SECTIONS)]
	sprite = ScaledSurface((4, 4), (0,0,0,0), SCALE, flags=pg.SRCALPHA)

	backgrounds[0].fill((220,220,220), pg.Rect(0, flip(25), 7, 1))
	backgrounds[2145 // HEIGHT].fill((220,220,220), pg.Rect(0, flip(2145), 7, 1))

	# Iterators
	jet = cycle(jets)
	shape = cycle(shapes)
	hue = (round(360 * i * GOLD_RAT) for i in count(1))
	next_section = 1

	# Arrays with pixel data
	tower = np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0]])
	draw_pixels(backgrounds[0], tower, (0,0,0), (255,255,255))
	rendering(window, backgrounds, sprite, [[0,0]], 5)

	block = next(shape).copy()
	draw_pixels(sprite, block, [next(hue)])
	block += [2, max(tower[:,1]) + 4]

	# Starting paused
	while not pg.key.get_pressed()[pg.K_SPACE]:
		e = pg.event.wait()
		if e.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
			pg.quit()
			return

	block_count = 0
	while rendering(window, backgrounds, sprite, block, block_count):
		movement = block + next(jet)
		is_blocked = (
			any(movement[:,0] == -1) or
			any(movement[:,0] == 7) or
			any_in(movement, tower)
		)
		if not is_blocked:
			block = movement

		movement = block + [0,-1]
		if not any_in(movement, tower):
			block = movement
			continue

		# Block landed
		block_count += 1
		tower = np.concatenate((tower, block))
		stamp_background(backgrounds, sprite, block)

		block = next(shape).copy()
		draw_pixels(sprite, block, [next(hue)])
		block += [2, max(tower[:,1]) + 4]

		# Clear sections that the sprite appears in.
		if max(block[:,1]) >= next_section * HEIGHT:
			i = next_section % SECTIONS
			backgrounds[i].fill((255,255,255))
			mask = section_masks(tower[:,1])[i]
			tower = tower[~mask]
			next_section += 1

def rendering(window:SurfaceType, backgrounds:list[ScaledSurface], sprite:ScaledSurface, pixels:PixelArray, i:int) -> bool:
	if pg.event.get(eventtype=pg.QUIT) or pg.key.get_pressed()[pg.K_ESCAPE]:
		pg.quit()
		return False

	# When the example data starts to repeat
	while i == 1415 and not pg.key.get_pressed()[pg.K_SPACE]:
		pg.event.wait()

	for _ in range(9):
		if pg.key.get_pressed()[pg.K_SPACE]:
			pg.time.delay(20)
		else: break
	pg.event.pump()

	for surface, x in zip(backgrounds, count(0, 8 * SCALE)):
		window.blit(surface.big, (x, 0))

	x, y = np.amin(pixels, axis=0)
	x1, x2 = x_surface_matches(x, y)
	y1, y2 = y_surface_matches(y)

	window.blits((
		sprite.big_coords(x1, y1),
		sprite.big_coords(x2, y2),
	))

	pg.display.update()
	pg.time.delay(0)
	return True

def draw_pixels(surface:ScaledSurface, pixels:PixelArray, hsv:Sequence[int], fillcolor=(0,0,0,0)) -> None:
	h = surface.get_height()
	surface.fill(fillcolor)
	for x, y in pixels:
		surface.set_at((x, flip(y, h)), hsv_to_rgb(*hsv))
	surface._stretch()

def stamp_background(backgrounds:list[ScaledSurface], sprite:ScaledSurface, pixels:PixelArray) -> None:
	"""Imprint the sprite onto the relevant backgrounds."""

	x, y = np.amin(pixels, axis=0)
	i1, i2 = section_matches(y)
	y1, y2 = y_surface_matches(y)

	backgrounds[i1].blit(sprite, (x, y1))
	backgrounds[i2].blit(sprite, (x, y2))

def hsv_to_rgb(hue:int, sat:int=60, val:int=60) -> list[int]:
	s = sat / 100
	v = val / 100

	def hue_trapezoid(degree:int) -> float:
		sawtooth = abs((degree % 360) - 180) / 60 - 1
		return clamp(sawtooth, 0, 1)

	normalized_rgb = (
		((hue_trapezoid(hue - corner) - 1) * s + 1) * v
		for corner in (0, 120, 240)
	)
	return [round(255 * channel) for channel in normalized_rgb]


# Helpful things.

"""Utilities for blitting the sprite to two sections at once.
Takes the sprite's bottom left corner in a bottom left coordinate system.
Return full window (unscaled) coordinates."""

def section_matches(y:int) -> tuple[int,int]:
	"""Indices of current and subsequent sections."""
	sec_steps = y // HEIGHT
	return tuple(i % SECTIONS for i in (sec_steps, sec_steps + 1))

def x_surface_matches(x:int, y:int) -> tuple[int,int]:
	return tuple(x + 8 * s for s in section_matches(y))

def y_surface_matches(y:int) -> tuple[int,int]:
	"""Assumes the sprite is 4 pixels tall."""
	y1 = flip(y) - 3
	return y1, y1 + HEIGHT


def flip(y:int, height:int=HEIGHT) -> int:
	"""Turns bottom left coordinates into top left.
	height defaults to full window (unscaled) size."""
	return height - 1 - (y % height)

def section_masks(y_coordinates:NDArray[Shape["*"], Int]) -> NDArray[Shape["SECTIONS, *"], Bool]:
	"""Returns one mask for each section."""
	wrapped = y_coordinates % (HEIGHT * SECTIONS)
	borders = np.arange(SECTIONS).reshape((SECTIONS,1)) * HEIGHT
	return np.logical_and(borders <= wrapped, wrapped < borders + HEIGHT)

def any_in(a:PixelArray, b:PixelArray) -> bool:
	"""Compares all combinations of sub-arrays (coordinates)."""
	for x in a:
		coord_match = x == b
		pixel_match = np.all(coord_match, axis=1)
		if any(pixel_match):
			return True
	return False

def clamp(x, low, high):
	return max(min(high, x), low)

def make_gameparts(title="Pygame window", window_size=(800,600)) -> SurfaceType:
	pg.init()
	pg.display.set_caption(title)
	# Passing None as the argument blocks all events.
	pg.event.set_blocked(None)
	pg.event.set_allowed(pg.QUIT)
	pg.event.set_allowed(pg.KEYDOWN)
	window = pg.display.set_mode(window_size)
	return window

if __name__ == "__main__":
	print()
	main()
