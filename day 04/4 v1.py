with open("4.txt", "r", newline="\n") as f:
	elfpairs = f.read().splitlines()

def elfparser(line:str) -> tuple:
	pair = line.split(",")

	def intervalparser(interval:str) -> tuple:
		return tuple(map(int, interval.split("-")))

	return tuple(map(intervalparser, pair))

values = list(map(elfparser, elfpairs))

# 1
def full_containment(intervals:tuple) -> bool:
	i1, i2 = intervals
	if i1[0] == i2[0] or i1[1] == i2[1]:
		return True
	else:
		lower = i1[0] > i2[0]
		upper = i1[1] < i2[1]
		return lower == upper

redundancies = map(full_containment, values)
print(sum(redundancies))

# Had to make some clear tests to figure out the function.
# testvals = [
# 	((5, 7), (5, 7)),
# 	((5, 7), (4, 7)),
# 	((5, 7), (6, 7)),
# 	((5, 7), (5, 6)),
# 	((5, 7), (5, 8)),
# 	((5, 7), (4, 6)),
# 	((5, 7), (6, 8)),
# 	((5, 7), (6, 6)),
# 	((5, 7), (4, 8)),
# ]
# for x in zip(testvals, [full_containment(val) for val in testvals]):
# 	print(x)

# 2
def partial_overlap(intervals):
	i1, i2 = intervals
	return not (i1[1] < i2[0] or i1[0] > i2[1])

some_redundancy = map(partial_overlap, values)
print(sum(some_redundancy))
