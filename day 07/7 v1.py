from operator import getitem, setitem
from functools import reduce

class nested_dict(dict):
	"""A dictionary where passing an iterable to the subscript operator
	will follow that path in a tree of nested dictionaries.

	Implementation should be identical for other collections such as lists.
	"""

	def __getitem__(self, keys):
		if not isinstance(keys, (list, tuple)):
			return super().__getitem__(keys)
		else:
			# Replace `self` with a regular dict to call the super method.
			# Otherwise this method would recurse.
			args = [dict(self)] + list(keys)
			return reduce(getitem, args)

	def __setitem__(self, keys, val):
		if not isinstance(keys, (list, tuple)):
			return super().__setitem__(keys, val)
		elif len(keys) == 1:
			return super().__setitem__(keys[0], val)
		else:
			current_dir = getitem(self, keys[:-1])
			return setitem(current_dir, keys[-1], val)

def process_logs(logs:list) -> dict:
	filestructure = nested_dict()
	# Current working directory inside the nested dict.
	cwd = []

	for line in logs:
		tokens = line.split()
		if tokens[0:2] == ["$", "cd"]:
			if tokens[2] == "/":
				cwd.clear()
			elif tokens[2] == "..":
				cwd.pop()
			else:
				cwd.append(tokens[2])

		elif tokens[0:2] == ["$", "ls"]:
			pass # no info for us here

		elif tokens[0] == "dir":
			filestructure[cwd + tokens[1:2]] = {}

		elif tokens[0].isnumeric():
			filestructure[cwd + tokens[1:2]] = int(tokens[0])

	return filestructure

def report_dirsizes(filestructure:dict, tally:list) -> int:
	dirtotal = 0

	for name, entry in filestructure.items():
		if type(entry) is dict:
			dirtotal += report_dirsizes(entry, tally)
		else:
			dirtotal += entry

	tally.append(dirtotal)
	return dirtotal

def main():
	with open("7.txt", "r", newline="\n") as f:
		console_logs = f.read().splitlines()

	filestructure = process_logs(console_logs)

	# Passing a mutable object to the function lets each
	# recursion update it without using a global variable.
	dirsizes = []
	report_dirsizes(filestructure, dirsizes)

	#1
	limited_sizes = [s for s in dirsizes if s <= 100000]
	print(sum(limited_sizes))

	# 2
	# The root directory is the last one to return,
	# so the last value is the total filesize.
	missing = dirsizes[-1] + 30000000 - 70000000
	large_enough_dirs = [s for s in dirsizes if s >= missing]
	print(min(large_enough_dirs))

if __name__ == "__main__":
	print()
	main()
