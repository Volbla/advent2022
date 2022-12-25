import re
from itertools import combinations, count, permutations, pairwise
from math import inf, comb
from numpy import cumsum
from time import perf_counter as clock
from typing import Sequence, Iterator

with open("16.txt", "r", newline="\n") as f:
	matches = re.findall(
		r"^Valve (\w\w) has flow rate=(\d+).+ valves? (.+)",
		f.read(),
		flags=re.MULTILINE)

flow_rate = {}; connections = {}
for line in matches:
	flow_rate[line[0]] = int(line[1])
	connections[line[0]] = tuple(line[2].split(", "))
operational_valves:set = {key for key, val in flow_rate.items() if val > 0}
def source_distances() -> dict:
	distances = {"AA": 0}
	current_depth = 0
	while True:
		additions = {}
		for node in distances:
			if distances[node] != current_depth:
				continue
			for con in connections[node]:
				if con not in distances:
					additions[con] = current_depth + 1

		if additions:
			distances.update(additions)
			current_depth += 1
		else:
			break

	return distances
all_source_dist = source_distances()
# Add 1 to include the time to open the valve.
source_dist = {key: all_source_dist[key] + 1 for key in operational_valves}

def main():
	# 1
	# path_lengths = complex_distances(30)
	# print(find_best_single_path(path_lengths))

	# 2
	path_lengths = complex_distances(26, keep_short_paths=True)
	print(len(path_lengths))

def complex_distances(time_limit:int, keep_short_paths:bool=False) -> dict:
	def complex_loop(previous:dict, count:int) -> dict:
		distances = {}
		to_discard = {}
		for valve_combo in combinations(operational_valves, count):
			comboset = frozenset(valve_combo)

			for addition in valve_combo:
				subcomboset = comboset.difference((addition,))
				if subcomboset not in previous:
					continue

				shortest = min([previous[frozenset((close_to, addition))] for close_to in subcomboset])
				newdist = previous[subcomboset] + shortest
				including_source = [newdist + source_dist[valve] < time_limit for valve in valve_combo]

				# Discarding short paths that are always a subset of a longer path.
				# Still keep pairs, since they're needed for later calculations.
				if not keep_short_paths and all(including_source) and count > 3:
					to_discard[subcomboset] = -1

				if any(including_source) and newdist < distances.get(comboset, inf):
					distances[comboset] = newdist
		distances.update(to_discard)
		return distances

	path_lengths = pairs_distances()
	node_count = iter(count(3))
	while newpaths := complex_loop(path_lengths, next(node_count)):
		print(len(newpaths))
		path_lengths.update(newpaths)
		for key, val in tuple(path_lengths.items()):
			if val == -1: del path_lengths[key]

	return path_lengths

def pairs_distances() -> dict:
	"""Includes the time it takes to open a valve after arrival."""

	distances = {}
	for v1, v2 in combinations(operational_valves, 2):
		key = frozenset((v1, v2))
		distances[key] = bread_search(v1, v2)

	return distances

def bread_search(start, goal) -> int:
	openSet = {start,}

	cameFrom = {}

	gScore = {}
	gScore[start] = 0

	while openSet:
		current = sorted(list(openSet), key=lambda x: gScore[x])[0]

		openSet.remove(current)
		for neighbor in connections[current]:
			tentative_gScore = gScore[current] + 1

			if tentative_gScore < gScore.get(neighbor, inf):
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore

				if neighbor not in openSet:
					openSet.add(neighbor)

	return measure_path(cameFrom, goal)

def measure_path(cameFrom, current):
	total_path = [current]

	while current in cameFrom.keys():
		current = cameFrom[current]
		total_path.append(current)

	return len(total_path)

if __name__ == "__main__":
	print()
	main()
