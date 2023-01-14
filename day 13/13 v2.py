from numpy import flatnonzero

T = int | list["T"]

with open("13.txt", "r", newline="\n") as f:
	inptext = f.read()
# for 1
signalpairs = [tuple(map(eval, pair.splitlines())) for pair in inptext.split("\n\n")]
# for 2
signals = [eval(line) for line in inptext.splitlines() if line]

def enclose(x:T) -> T:
	if isinstance(x, list):
		return x
	return [x]

def difference_if(a:T, b:T) -> int:
	aint = isinstance(a, int)
	bint = isinstance(b, int)

	if aint and bint:
		return a - b

	elif aint or bint:
		return difference_if(enclose(a), enclose(b))

	else:
		for a_elem, b_elem in zip(a, b):
			if (response := difference_if(a_elem, b_elem)) != 0:
				return response

		return len(a) - len(b)

def difference_match(left:T, right:T) -> int:
	match (left, right):
		case (int(l), int(r)):
			return l - r

		case (int(x), list(y)) | (list(x), int(y)):
			return difference_match(enclose(x), enclose(y))

		case (list(xs), list(ys)):
			for l, r in zip(xs, ys):
				if (res := difference_match(l, r)) != 0:
					return res

			return len(xs) - len(ys)

	return 0

# Correct outputs:
# 5605
# 24969

for f in (difference_if, difference_match):
	# 1
	in_correct_order = [f(*pair) < 0 for pair in signalpairs]
	print(sum(flatnonzero(in_correct_order) + 1))

	# 2
	sorted_signals:list[T] = [[[2]], [[6]]]

	for s in signals:
		for i, ss in enumerate(sorted_signals):
			if f(s, ss) < 0:
				sorted_signals.insert(i, s)
				break
	# There's no need to append unsorted signals to the end
	# since that doesn't affect the indices of [[2]] and [[6]].

	divider1 = sorted_signals.index([[2]]) + 1
	divider2 = sorted_signals.index([[6]]) + 1

	print(divider1 * divider2)
