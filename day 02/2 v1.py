with open("2.txt", "r", newline="\n") as f:
	rounds = [line.split() for line in f]

# 1
elfcode = {"A":0, "B":1, "C":2}
mancode = {"X":0, "Y":1, "Z":2}

def result(elf, man):
	e, m = elfcode[elf], mancode[man]
	shapepoints = m + 1

	wincode = (m - e) % 3
	# A code of 0 means no difference: draw
	# 1 higher than the elf: win.
	# 2 higher is the same as one lower: loss
	outcomepoints = (
		0 if wincode == 2 else
		3 if wincode == 0 else
		6 # if wincode == 1
	)

	return shapepoints + outcomepoints

points = [result(*rpsround) for rpsround in rounds]
print(sum(points))

# 2
# Can be read as (-1, 0, 1) mod 3
outcomecode = {"X":2, "Y":0, "Z":1}

def resultupdate(elf, outcome):
	e, o = elfcode[elf], outcomecode[outcome]
	# Same as before
	outcomepoints = (
		0 if o == 2 else
		3 if o == 0 else
		6 # if o == 1
	)

	shapecode = (e + o) % 3
	shapepoints = shapecode + 1

	return shapepoints + outcomepoints

points2 = [resultupdate(*rpsround) for rpsround in rounds]
print(sum(points2))
