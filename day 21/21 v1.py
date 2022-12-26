from operator import add, sub, mul, floordiv
from itertools import pairwise

with open("21.txt", "r", newline="\n") as f:
	inptext = f.read().splitlines()
example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".splitlines()
matchop = {"+": add, "-": sub, "*": mul, "/": floordiv}

def main():
	done = {}
	waiting = {}

	for line in inptext:
		monkey, _, job = line.partition(": ")
		if job.isnumeric():
			done[monkey] = int(job)
		else:
			m1, op, m2 = job.split()
			waiting[monkey] = (m1, matchop[op], m2)

	# 1
	answer = calculate_root(done, waiting, "root")
	print(answer)

	# Checking how often each monkey appears.
	# Besides "root" they all appear twice,
	# so they're referenced only once.
	import re
	from numpy import unique
	monks = re.findall(r"[a-z]{4}", " ".join(inptext))
	w, c = unique(monks, return_counts=True)
	n, c2 = unique(c, return_counts=True)
	print(n, c2, w[c == 1])

	# 2
	newdone, newwait = reverse_from_node(done, waiting, "humn")
	humn_answer = calculate_root(newdone, newwait, "humn")
	print(humn_answer)

def calculate_root(a:dict, b:dict, target:str) -> float:
	done, waiting = a.copy(), b.copy()

	while target not in done:
		heck = list(waiting.keys())
		for monkey in heck:
			m1, op, m2 = waiting[monkey]
			if (m1 in done) and (m2 in done):
				done[monkey] = op(done[m1], done[m2])
				waiting.pop(monkey)

	return done[target]

def reverse_from_node(a:dict, b:dict, target:str) -> tuple[dict,dict]:
	done, waiting = a.copy(), b.copy()
	done.pop(target, None)
	waiting.pop(target, None)

	reverse_path = (
		{val[0]: key for key, val in waiting.items()} |
		{val[2]: key for key, val in waiting.items()}
	)
	humn_path = [target]
	while humn_path[-1] != "root":
		humn_path.append(reverse_path[humn_path[-1]])

	reverse_op = {sub: add, add: sub, floordiv: mul, mul: floordiv}

	for monkey, parent in pairwise(humn_path):
		old_job = waiting.pop(parent)
		op = old_job[1]
		# indexing monkeys
		this_monk = (monkey == old_job[2]) * 2
		other_monk = (not this_monk) * 2

		if this_monk == 2 and op in (sub, floordiv):
			waiting[monkey] = (old_job[other_monk], op, parent)
		else:
			waiting[monkey] = (parent, reverse_op[op], old_job[other_monk])

	# Making "root" not modify its companion.
	root_job = list(waiting[humn_path[-2]])
	root_job[1] = add
	waiting[humn_path[-2]] = tuple(root_job)
	done["root"] = 0

	return done, waiting

if __name__ == "__main__":
	print()
	main()
