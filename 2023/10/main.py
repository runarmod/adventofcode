import itertools
import time
from collections import defaultdict
import networkx as nx


def parseLine(line, y, height):
    all_dirs = defaultdict(set)
    for x, c in enumerate(line):
        if c == ".":
            continue
        dirs = []
        if c == "|":
            dirs.append((x, y + 1))
            dirs.append((x, y - 1))
        elif c == "-":
            dirs.append((x - 1, y))
            dirs.append((x + 1, y))
        elif c == "L":
            dirs.append((x, y - 1))
            dirs.append((x + 1, y))
        elif c == "J":
            dirs.append((x, y - 1))
            dirs.append((x - 1, y))
        elif c == "7":
            dirs.append((x, y + 1))
            dirs.append((x - 1, y))
        elif c == "F":
            dirs.append((x, y + 1))
            dirs.append((x + 1, y))
        elif c == "S":
            dirs.append((x, y + 1))
            dirs.append((x, y - 1))
            dirs.append((x - 1, y))
            dirs.append((x + 1, y))
        for d in dirs:
            if 0 <= d[0] < len(line) and 0 <= d[1] < height:
                all_dirs[(x, y)].add(d)
    return all_dirs


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.parse(filename)

    def parse(self, filename):
        self.f = open(filename).read().rstrip().split("\n")

        self.start = next(
            filter(
                lambda z: self.f[z[1]][z[0]] == "S",
                itertools.product(range(len(self.f[0])), range(len(self.f))),
            ),
        )

        neighbours = defaultdict(set)
        for line in [parseLine(line, y, len(self.f)) for y, line in enumerate(self.f)]:
            for k, v in line.items():
                for v2 in v:
                    neighbours[k].add(v2)

        # The map should be undirected, so I create an edge if to nodes points to each other.
        _map = [
            ((x, y), (x + dx, y + dy))
            for x, y in itertools.product(range(len(self.f[0])), range(len(self.f)))
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))
            if 0 <= x + dx < len(self.f[0])
            and 0 <= y + dy < len(self.f)
            and (x + dx, y + dy) in neighbours[(x, y)]
            and (x, y) in neighbours[(x + dx, y + dy)]
        ]

        self.graph = nx.Graph(_map)

    def part1(self):
        return max(
            nx.single_source_shortest_path_length(self.graph, self.start).values()
        )

    def part2(self):
        cycle_dict = self.create_cycle_dict(self.graph)
        inside = 0
        for y in range(len(self.f)):
            for x in range(len(self.f[y])):
                if (x, y) in cycle_dict.keys():
                    continue
                cycles = []
                for n in range(x - 1, -1, -1):
                    if (n, y) in cycle_dict.keys():
                        cycles.append((n, y))
                inside += self.count_crossings_right_to_left(cycles, cycle_dict) % 2
        return inside

    def create_cycle_dict(self, graph):
        cycle_graph = nx.find_cycle(graph)
        cycle_dict = defaultdict(set)
        for fr, to in cycle_graph:
            cycle_dict[fr].add(to)
            cycle_dict[to].add(fr)
        return cycle_dict

    def count_crossings_right_to_left(self, cycles, cycle_dict):
        """
        Crossing the cycle line an odd number of times means we are inside the cycle.
        To determine if we are inside the cycle, we need to count the number of times
        we cross the cycle line. However, we need to be careful about the direction
        of cycle line when crossing. For example, if we cross the cycle line from
        right to left, and encounter a "|", we know we cross from in to out, or out
        to in. If we encounter a "-", our side does not change. If we encounter a
        "J" then "L" (from the left, looking like "LJ" in the graph), we know we
        do not cross the cycle line (same with "F7"). If we encounter a "J" then
        "F" ("FJ"), we know we cross the cycle line (same with "L7").
        """

        # Start with turning coords to letters to better visualize the problem
        cycles_letters = self.create_letters_from_cycle_coord(cycles, cycle_dict)

        # Want to combine all crossings to "|"'s, so we can count the number of
        # real crossings by counting the number of "|"'s.
        while not all(c == "|" for c in cycles_letters):
            _new = []
            i = 0
            while i < len(cycles_letters):
                # Direct crossing:
                if cycles_letters[i] == "|":
                    _new.append("|")
                    i += 1
                elif i == len(cycles_letters) - 1:
                    i += 1
                # Indirect crossings:
                elif cycles_letters[i] == "L" and cycles_letters[i + 1] == "7":
                    i += 2
                    cycles_letters.append("|")
                elif cycles_letters[i] == "F" and cycles_letters[i + 1] == "J":
                    i += 2
                    cycles_letters.append("|")
                # Non-crossings:
                elif cycles_letters[i] == "F" and cycles_letters[i + 1] == "7":
                    i += 2
                elif cycles_letters[i] == "L" and cycles_letters[i + 1] == "J":
                    i += 2
            cycles_letters = _new
        return len(cycles_letters)

    def create_letters_from_cycle_coord(self, cycles, cycle_dict):
        # Could check self.f to determine the letters, but this was the first
        # solution I came up with, and it works. Also, it handles "S" automatically
        # by looking at all coords in the cycle's neighbours.
        cycles_letters = []
        for x, y in cycles:
            if len({(x - 1, y), (x + 1, y)} & cycle_dict[(x, y)]) == 2:  # -
                continue
            if len({(x, y - 1), (x, y + 1)} & cycle_dict[(x, y)]) == 2:  # |
                cycles_letters.append("|")
            if len({(x - 1, y), (x, y - 1)} & cycle_dict[(x, y)]) == 2:  # J
                cycles_letters.append("J")
            if len({(x + 1, y), (x, y - 1)} & cycle_dict[(x, y)]) == 2:  # L
                cycles_letters.append("L")
            if len({(x - 1, y), (x, y + 1)} & cycle_dict[(x, y)]) == 2:  # 7
                cycles_letters.append("7")
            if len({(x + 1, y), (x, y + 1)} & cycle_dict[(x, y)]) == 2:  # F
                cycles_letters.append("F")

        # The letters are stored right to left for the direction right to left in
        # the graph, so reverse to better visualize.
        return cycles_letters[::-1]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
