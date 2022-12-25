with open("10.txt", "r", newline="\n") as f:
	inp = f.read().split()

value_changes = [0 if word.isalpha() else int(word) for word in inp]
value_changes[0] = 1

# 1
target_cycles = (n * 40 + 20 for n in range(6))
signal_strengths = [sum(value_changes[:cycle - 1]) * cycle for cycle in target_cycles]

print(sum(signal_strengths))

# 2
import numpy as np

# Realigning
value_changes[0] = 0
value_changes.insert(0, 1)
value_changes.pop()

center_pos = np.cumsum(value_changes)
sprite_pos = np.stack((
	center_pos - 1,
	center_pos,
	center_pos + 1
), axis=0)

pixel_pos = np.arange(6 * 40) % 40
is_drawn = np.any(sprite_pos == pixel_pos, axis=0)

print(is_drawn.reshape((6,40)).astype(int))
