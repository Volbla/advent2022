with open("3.txt", "r", newline="\n") as f:
	rucksacks = f.read().splitlines()

oa, oA = ord("a"), ord("A")
def pointconversion(c:str) -> int:
	num = ord(c)
	if num >= oa:
		return num - oa + 1
	else:
		return num - oA + 27

# 1
overlaps = []
for sack in rucksacks:
	l = len(sack) // 2
	comp1, comp2 = sack[:l], sack[l:]
	shared = set(comp1) & set(comp2)
	overlaps.append(shared.pop())

prio = map(pointconversion, overlaps)
print(sum(prio))

# 2
from functools import reduce

def findbadge(group:list) -> str:
	setlist = [set(s) for s in group]
	badgeset = reduce(set.intersection, setlist)
	return badgeset.pop()

def sliced(seq, n):
	"""Iterator of consecutive slices of size n"""
	return (seq[i:i+n] for i in range(0, len(seq), n))

groupbadges = map(findbadge, sliced(rucksacks, 3))
groupprio = map(pointconversion, groupbadges)
print(sum(groupprio))
