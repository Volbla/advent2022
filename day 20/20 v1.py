import numpy as np
from numpy import array
from itertools import product

with open("20.txt", "r", newline="\n") as f:
	encrypted = [int(x) for x in f.readlines()]
# Site example
# encrypted = [1,2,-3,3,-2,0,4]

def main():
	l = len(encrypted)

	# 1
	out = decrypt(encrypted)
	zero = np.flatnonzero(out == 0)[0]
	x, y, z = out[(zero + 1000) % l], out[(zero + 2000) % l], out[(zero + 3000) % l]
	print(x+y+z)

	# 2
	out2 = decrypt_big(encrypted)
	zero = np.flatnonzero(out2 == 0)[0]
	x, y, z = out2[(zero + 1000) % l], out2[(zero + 2000) % l], out2[(zero + 3000) % l]
	print(x+y+z)

def decrypt(data):
	l = len(data)
	diagonal = np.eye(l, dtype=int) * data

	for i in range(l):
		if i % 100 == 0 and i != 0:
			print(i)

		try:
			j = np.flatnonzero(diagonal[i,:])[0]
		except IndexError:
			# A row of all zeros returns an empty list.
			continue

		move = diagonal[i,j]
		to = (j + move) % (l - 1)

		if to > j:
			diagonal[:,j:to+1] = np.roll(diagonal[:,j:to+1], -1, axis=1)
		if to < j:
			diagonal[:,to:j+1] = np.roll(diagonal[:,to:j+1], 1, axis=1)

	return np.sum(diagonal, axis=0)

def decrypt_big(data):
	l = len(data)
	dt = np.min_scalar_type(-811589153 * max(map(abs, data)))
	diagonal = np.eye(l, dtype=dt) * data * 811589153

	for i0 in range(10 * l):
		i = i0 % l
		if i0 % 100 == 0 and i0 != 0:
			print(i0)

		try:
			j = np.flatnonzero(diagonal[i,:])[0]
		except IndexError:
			continue

		move = diagonal[i,j]
		to = (j + move) % (l - 1)

		if to > j:
			diagonal[:,j:to+1] = np.roll(diagonal[:,j:to+1], -1, axis=1)
		if to < j:
			diagonal[:,to:j+1] = np.roll(diagonal[:,to:j+1], 1, axis=1)

	return np.sum(diagonal, axis=0)

if __name__ == "__main__":
	print()
	main()
