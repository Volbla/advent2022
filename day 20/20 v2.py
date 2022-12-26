import numpy as np
from numpy import array

with open("20.txt", "r", newline="\n") as f:
	encrypted = [int(x) for x in f.readlines()]
# Site example
# encrypted = [1,2,-3,3,-2,0,4]

def main():
	# Turns out manipulating two arrays is faster than five thousand.
	l = len(encrypted)

	with_key = array(encrypted, dtype=np.int64) * 811589153

	for data, reps in zip((encrypted, with_key), (1, 10)):
		out = decrypt(data, reps)
		zero = np.flatnonzero(out == 0)[0]
		x, y, z = out[(zero + 1000) % l], out[(zero + 2000) % l], out[(zero + 3000) % l]
		print(x+y+z)

def decrypt(data, reps):
	l = len(data)
	stuff = np.vstack((np.arange(l), data))

	for i in range(l * reps):
		j = np.flatnonzero(stuff[0,:] == (i % l))[0]

		move = stuff[1,j]
		to = (j + move) % (l - 1)

		if to > j:
			stuff[:,j:to+1] = np.roll(stuff[:,j:to+1], -1, axis=1)
		if to < j:
			stuff[:,to:j+1] = np.roll(stuff[:,to:j+1], 1, axis=1)

	return stuff[1,:]

if __name__ == "__main__":
	print()
	main()
