from typing import Self, Callable
import re

def main():
	with open("11.txt", "r", newline="\n") as f:
		monkey_strings = f.read().split("\n\n")

	monkeys = []
	for ms in monkey_strings:
		lines = ms.splitlines()
		if not lines[0].startswith("Monkey"):
			raise ValueError("Not a monkey string.")

		data = {}
		data["items"] = parse_items(lines[1])
		data["operation"] = parse_operation(lines[2])
		data["test"] = parse_test(lines[3:])

def parse_items(s:str) -> list[int]:
	if not s.strip().startswith("Starting items"):
		raise ValueError("Not an item string.")

	worry_lvl = re.finditer(r"\d+", s)
	return [int(x) for x in worry_lvl]

def parse_operation(s:str) -> Callable:
	s1 = s.strip().partition(" = ")
	if not s1[0].startswith("Operation"):
		raise ValueError("Not an operation string.")

	if re.fullmatch(r"(old|\d+) ?(\+|\*) ?(old|\d+)", s1[2]):
		return lambda old: eval(s1[2])
	else:
		raise ValueError("Not an allowed operation.")

def parse_test(ls:list[str]) -> Callable:
	pass

if __name__ == "__main__":
	print()
	main()
