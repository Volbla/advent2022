with open("1.txt", "r", newline="\n") as f:
	elfstrings = f.read().split("\n\n")

elves = [(int(s) for s in elf.splitlines()) for elf in elfstrings]

# 1
total = [sum(elf) for elf in elves]
print(max(total))

# 2
total.sort(reverse=True)
print(total[:3])
print(sum(total[:3]))
