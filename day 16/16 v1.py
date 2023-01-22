import re
from itertools import combinations, count, permutations, pairwise
from math import inf, comb
from numpy import cumsum
from time import perf_counter as clock

with open("16.txt", "r", newline="\n") as f:
	matches = re.findall(
		r"^Valve (\w\w) has flow rate=(\d+).+ valves? (.+)",
		f.read(),
		flags=re.MULTILINE)

flow_rate: dict[str,int] = {}; connections: dict[str,tuple[str]] = {}
for line in matches:
	flow_rate[line[0]] = int(line[1])
	connections[line[0]] = tuple(line[2].split(", "))

operational_valves: set[str] = {key for key, val in flow_rate.items() if val > 0}

def source_distances() -> dict:
	"""Shortest distance from each node to the source."""

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
source_dist: dict[str,int] = {key: all_source_dist[key] + 1 for key in operational_valves}

def main():
	# 1
	path_lengths = complex_distances(30)
	print(find_best_single_path(path_lengths))

	# 2 This took me almost 4 hours to compute.
	path_lengths = complex_distances(26, keep_short_paths=True)
	print(find_best_double_path(path_lengths))

def find_best_single_path(paths:dict[frozenset,int]) -> int:
	paths_count = len(paths)
	c = iter(count()); past = clock()

	most_pressure = 0
	for nodes in paths:
		# Track progress.
		paths_finished = next(c)
		if clock() - past > 2:
			past = clock()
			print(f"{paths_finished}/{paths_count}", len(nodes))

		most_pressure = max(most_pressure, pressure_from_best_order(paths, nodes, 30))

	return most_pressure

def find_best_double_path(paths:dict) -> int:
	paths_count = comb(len(paths), 2)
	c = iter(count()); past = clock()

	most_pressure = 0
	for man_nodes, elephant_nodes in combinations(paths, 2):
		# Track progress.
		paths_finished = next(c)
		if clock() - past > 10:
			past = clock()
			print(f"{paths_finished}/{paths_count}", len(man_nodes), len(elephant_nodes))

		# Skip any paths that overlap.
		if set(man_nodes) & set(elephant_nodes):
			continue

		man_pressure = pressure_from_best_order(paths, man_nodes, 26)
		elephant_pressure = pressure_from_best_order(paths, elephant_nodes, 26)
		most_pressure = max(most_pressure, man_pressure + elephant_pressure)

	return most_pressure

def pressure_from_best_order(path_lengths:dict, nodes:frozenset, time_limit:int) -> int:
	most_pressure = 0
	for first in nodes:
		from_source = source_dist[first]
		if not path_lengths[nodes] + from_source < time_limit:
			continue

		back = list(nodes)
		back.remove(first)
		for backorder in permutations(back):
			order = (first, ) + backorder

			delays = cumsum(
				[from_source] +
				[path_lengths[frozenset(pair)] for pair in pairwise(order)]
			)
			released_pressure = sum([
				(time_limit - delay) * flow_rate[valve]
				for valve, delay in zip(order, delays)
			])
			most_pressure = max(most_pressure, released_pressure)
	return most_pressure

def complex_distances(time_limit:int, keep_short_paths:bool=False) -> dict[frozenset,int]:

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

				# Discard short paths that are subsets of all longer paths.
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
		path_lengths.update(newpaths)
		for key, val in tuple(path_lengths.items()):
			if val == -1: del path_lengths[key]

	return path_lengths

def pairs_distances() -> dict[frozenset,int]:
	"""Includes the time it takes to open a valve after arrival."""

	distances = {}
	for v1, v2 in combinations(operational_valves, 2):
		key = frozenset((v1, v2))
		distances[key] = bread_search(v1, v2)

	return distances

def bread_search(start:str, goal:str) -> int:
	openSet = {start,}

	cameFrom = {}

	gScore = {}
	gScore[start] = 0

	while openSet:
		current = min(openSet, key=lambda x: gScore[x])

		openSet.remove(current)
		for neighbor in connections[current]:
			tentative_gScore = gScore[current] + 1

			if tentative_gScore < gScore.get(neighbor, inf):
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore

				if neighbor not in openSet:
					openSet.add(neighbor)

	return measure_path(cameFrom, goal)

def measure_path(cameFrom:dict, current:str) -> int:
	total_path = [current]

	while current in cameFrom.keys():
		current = cameFrom[current]
		total_path.append(current)

	return len(total_path)

def onewayconnections() -> list[str]:
	"""Formats node connections for pasting into GraphViz."""

	def loop(node, pathlist, paths):
		deeper = [con for con in connections[node] if source_dist[con] > source_dist[node]]
		if not deeper:
			paths.append(tuple(pathlist))
			return

		for next_node in deeper:
			pathlist.append(next_node)
			loop(next_node, pathlist, paths)
			pathlist.pop()

	templist = ["AA"]
	paths = []
	loop("AA", templist, paths)

	graphbjoms = []
	for path in paths:
		for pair in pairwise(path):
			if pair not in graphbjoms:
				graphbjoms.append(pair)

	for key, cons in connections.items():
		for con in cons:
			if source_dist[key] == source_dist[con] and (con, key) not in graphbjoms:
				graphbjoms.append((key, con))
				print(1, end=" ")

	things = [f'  "{a}: {flow_rate[a]}" -- "{b}: {flow_rate[b]}";' for a, b in graphbjoms]

	return things

if __name__ == "__main__":
	print()
	main()
