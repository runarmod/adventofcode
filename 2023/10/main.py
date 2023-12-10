from functools import lru_cache
import itertools
import time
from collections import defaultdict
import networkx as nx


def parseLine(line, y, height):
    all_dirs: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for x, c in enumerate(line):
        if c == ".":
            continue
        dirs = []
        if c in "|7FS":
            dirs.append((x, y + 1))
        if c in "|LJS":
            dirs.append((x, y - 1))
        if c in "-J7S":
            dirs.append((x - 1, y))
        if c in "-LFS":
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

        neighbours: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(
            set
        )
        for line in [parseLine(line, y, len(self.f)) for y, line in enumerate(self.f)]:
            for k, v in line.items():
                for v2 in v:
                    neighbours[k].add(v2)

        self.graph: "nx.Graph" = nx.DiGraph(neighbours).to_undirected(reciprocal=True)

        self.cycle_dict = self.create_cycle_dict(self.graph)

    def part1(self):
        return max(
            nx.single_source_shortest_path_length(self.graph, self.start).values()
        )

    def part2(self):
        """
        Find the number of coords inside the graph (the cycle line should not be counted).
        """
        return sum(
            self.inside(
                tuple((n, y) for n in range(x - 1, -1, -1) if (n, y) in self.cycle_dict)
            )
            for y in range(len(self.f))
            for x in range(len(self.f[y]))
            if (x, y) not in self.cycle_dict
        )

    def create_cycle_dict(
        self, graph: "nx.Graph"
    ) -> defaultdict[tuple[int, int], set[tuple[int, int]]]:
        cycle_graph: list[tuple[tuple[int, int], tuple[int, int]]] = nx.find_cycle(
            graph
        )
        cycle_dict: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(
            set
        )
        for fr, to in cycle_graph:
            cycle_dict[fr].add(to)
            cycle_dict[to].add(fr)
        return cycle_dict

    def inside(self, cycles: list[tuple[int, int]]) -> bool:
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

        Therefore we can check if the sum of "|", "F" and "7" is odd, and if so,
        we are inside the cycle.
        """
        cycles_letters = self.create_letters_from_cycle_coord(tuple(cycles))
        return sum(cycles_letters.count(letter) for letter in "|F7") % 2

    @lru_cache(maxsize=None)
    def create_letters_from_cycle_coord(
        self, cycles: tuple[tuple[int, int], ...]
    ) -> str:
        # Could check self.f to determine the letters, but this was the first
        # solution I came up with, and it works. Also, it handles "S" automatically
        # by looking at all coords in the cycle's neighbours.

        if len(cycles) == 0:
            return ""

        _next = self.create_letters_from_cycle_coord(cycles[:-1])
        neighbors = self.cycle_dict[cycles[-1]]
        x, y = cycles[-1]

        if len({(x - 1, y), (x + 1, y)} & neighbors) == 2:  # -
            return "" + _next
        if len({(x, y - 1), (x, y + 1)} & neighbors) == 2:  # |
            return "|" + _next
        if len({(x - 1, y), (x, y - 1)} & neighbors) == 2:  # J
            return "J" + _next
        if len({(x + 1, y), (x, y - 1)} & neighbors) == 2:  # L
            return "L" + _next
        if len({(x - 1, y), (x, y + 1)} & neighbors) == 2:  # 7
            return "7" + _next
        if len({(x + 1, y), (x, y + 1)} & neighbors) == 2:  # F
            return "F" + _next
        assert False, "Should not happen"


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
