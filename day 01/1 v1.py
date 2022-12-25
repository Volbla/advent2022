import string

elves = [[]]
with open("1.txt", "r", newline="\n") as f:
	for line in f:
		if line.strip(string.whitespace):
			ration = int(line)
			elves[-1].append(ration)
		else:
			elves.append([])

# 1
total = [sum(elf) for elf in elves]
print(max(total))

# 2
total.sort(reverse=True)
print(total[:3])
print(sum(total[:3]))