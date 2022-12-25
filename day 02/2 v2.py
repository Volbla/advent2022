with open("2.txt", "r", newline="\n") as f:
	rounds = [line.split() for line in f]

def code(letter:str) -> int:
	return "ABCXYZ".index(letter) % 3

elf = [code(x[0]) for x in rounds]
man = [code(x[1]) for x in rounds]
points1 = sum([
	3 * ((m - e + 1) % 3)
	+ m + 1
	for e, m in zip(elf, man)
])

outcome = man
points2 = sum([
	3 * o
	+ (e + o - 1) % 3 + 1
	for e, o in zip(elf, outcome)
])

print(points1, points2)
