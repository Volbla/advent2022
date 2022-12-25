import re
with open("5.txt", "r", newline="\n") as f:
	inp1, inp2 = f.read().split("\n\n")
cratestring = inp1.splitlines()
instructionstring = inp2.splitlines()

crates = []
for chars in zip(*cratestring):
	if chars[-1].isdigit():
		stack = [c for c in chars[-2::-1] if c.isalpha()]
		crates.append(stack)

parser = re.compile(r"move (\d+) from (\d) to (\d)")
instructions = []
for line in instructionstring:
	matchobj = re.match(parser, line)
	inst = map(int, matchobj.group(1, 2, 3))
	indexinst = [n - i for n, i in zip(inst, (0, 1, 1))]
	instructions.append(indexinst)

for inst in instructions:
	# quantity, source, destination
	n, s, d = inst

	crane = crates[s][-n:]
	del crates[s][-n:]
	# crane.reverse() # Only for part 1
	crates[d].extend(crane)

tops = [pile[-1] if pile else "_" for pile in crates]
print("".join(tops))
