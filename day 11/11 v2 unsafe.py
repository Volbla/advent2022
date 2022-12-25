from typing import Self, Callable
import re
from itertools import product, count
from operator import itemgetter

def parse_items(s:str) -> list[int]:
	worry_lvl = re.finditer(r"\d+", s)
	return [int(match[0]) for match in worry_lvl]

def parse_operation(s:str) -> Callable:
	op = s.strip().partition(" = ")[2]
	# 1
	# return lambda old: eval(op) // 3
	# 2
	# if op == "old * old":
	# 	return lambda old: old
	return lambda old: eval(op)

def parse_test(ls:list[str]) -> Callable:
	# mod, true, false
	M, T, F = [int(re.search(r"\d+", s)[0]) for s in ls]
	return lambda x: T if x % M == 0 else F


with open("11.txt", "r", newline="\n") as f:
	inp = f.read().split("\n\n")

monkeys:list[dict] = []
total_multiple = 1
for s in inp:
	lines = s.splitlines()

	data = {}
	data["items"] = parse_items(lines[1])
	data["operation"] = parse_operation(lines[2])
	data["test"] = parse_test(lines[3:])
	data["inspections"] = 0

	monkeys.append(data)
	# 2
	# Should also check for common factors if they weren't all prime.
	total_multiple *= int(re.search(r"\d+", lines[3])[0])

# print(total_multiple)
from time import perf_counter as p

s = p()
icache = 0
for i, monkey in product(range(4000), monkeys):
	for item in monkey["items"]:
		monkey["inspections"] += 1
		worry_lvl = monkey["operation"](item) % total_multiple
		target = monkey["test"](worry_lvl)
		monkeys[target]["items"].append(worry_lvl)
	monkey["items"].clear()

	if i % 1000 == 0 and i != icache:
		print(p() - s)
		s = p()
		icache = i

# besties = [(n, m["inspections"]) for n, m in zip(count(), monkeys)]
# besties.sort(key=itemgetter(1), reverse=True)
# print(besties[0][1] * besties[1][1])
