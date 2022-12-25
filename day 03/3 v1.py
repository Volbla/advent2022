with open("3.txt", "r", newline="\n") as f:
	rucksacks = f.read().splitlines()

def pointconversion(c:str) -> int:
	num = ord(c)
	if num >= 97:
		return num - 96
	else:
		return num - 65 + 27

# 1
overlaps = []
for sack in rucksacks:
	l = len(sack) // 2
	comp1, comp2 = sack[:l], sack[l:]
	shared = set(comp1) & set(comp2)
	# The compartments should share only one item.
	overlaps.append(shared.pop())

prio = map(pointconversion, overlaps)
print(sum(prio))

# 2
from functools import reduce

def compose(*functions):
	return reduce(lambda f, g: lambda x: g(f(x)), functions)

findbadge = compose(
	lambda stringlist: map(set, stringlist),
	lambda setlist: reduce(set.intersection, setlist),
	# The badge should be only one item.
	lambda oneset: oneset.pop()
)

def sliced(seq, n):
	"""Iterator of consecutive slices of size n"""
	return (seq[i:i+n] for i in range(0, len(seq), n))

groupbadges = [findbadge(group) for group in sliced(rucksacks, 3)]

groupprio = map(pointconversion, groupbadges)
print(sum(groupprio))
