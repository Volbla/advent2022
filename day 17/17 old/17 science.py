import numpy as np
from itertools import pairwise

with open("17.txt", "r", newline="\n") as f:
	inptext = f.read().strip()
exampletext = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

inarow = [1]
for a, b in pairwise(exampletext):
	if a == b:
		inarow[-1] += 1
	else:
		inarow.append(1)

# rowrow = np.array(inarow)
# print(np.unique(rowrow, return_counts=True))

textrow = map(str, inarow)
bignum = "".join(textrow)
print(bignum)

# onesides = []
# for i, c in enumerate(bignum):
# 	if c == "1": onesides.append(bignum[i - 1] + bignum[i + 1])

# print(np.unique(onesides, return_counts=True))
