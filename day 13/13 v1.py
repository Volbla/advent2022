from numpy import flatnonzero

with open("13.txt", "r", newline="\n") as f:
	inptext = f.read()
# for 1
signalpairs = (tuple(map(eval, pair.splitlines())) for pair in inptext.split("\n\n"))
# for 2
signals = (eval(line) for line in inptext.splitlines() if line)

def compare(a:int|list, b:int|list) -> None|bool:
	"""Returning None means the current comparison is inadequate
	and the search for order must go deeper."""

	are_ints = (type(a) is int, type(b) is int)

	if sum(are_ints) == 2:
		if a == b:
			return None
		else: return a < b

	elif sum(are_ints) == 1:
		if are_ints[0] == True:
			return compare([a], b)
		else:
			return compare(a, [b])

	elif sum(are_ints) == 0:
		for a2, b2 in zip(a, b):
			if (response := compare(a2, b2)) is not None:
				return response

		if (la := len(a)) == (lb := len(b)):
			return None
		else: return la < lb

# 1
correct = [compare(*pair) for pair in signalpairs]
print(sum(flatnonzero(correct) + 1))

# 2
sorted_signals = [[[2]], [[6]]]

for s in signals:
	for i, ss in enumerate(sorted_signals):
		if compare(s, ss):
			sorted_signals.insert(i, s)
			break
# Don't even need to append unsorted signals to the end
# since that doesn't change the indices of [[2]] and [[6]].

divider1 = sorted_signals.index([[2]]) + 1
divider2 = sorted_signals.index([[6]]) + 1

print(divider1 * divider2)
