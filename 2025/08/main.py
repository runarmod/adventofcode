import functools
import heapq
import itertools
import re
import time

import networkx
from aoc_utils_runarmod import get_data


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def numsNested(
    data: str | list[str] | list[list[str]],
) -> tuple[int | tuple[int, ...], ...]:
    if isinstance(data, str):
        return nums(data)
    if not hasattr(data, "__iter__"):
        raise ValueError("Data must be a tuple/list/iterable or a string")
    return tuple(e[0] if len(e) == 1 else e for e in filter(len, map(numsNested, data)))


def euclidean(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = [
            line.split(",")
            for line in get_data(2025, 8, test=test).strip("\n").split("\n")
        ]

        self.data = numsNested(self.data)
        self.G = networkx.Graph()
        for a, b in itertools.combinations(self.data, 2):
            self.G.add_edge(
                a,
                b,
                weight=euclidean(a, b),
            )

    def part1(self):
        new_G = networkx.Graph()
        q = [(x[2]["weight"], x) for x in self.G.edges(data=True)]

        for _, edge in heapq.nsmallest(1000 if not self.test else 10, q):
            new_G.add_edge(edge[0], edge[1])

        largest_components = heapq.nlargest(
            3, list(map(len, networkx.connected_components(new_G)))
        )
        return functools.reduce(lambda x, y: x * y, largest_components)

    def part2(self):
        new_G = networkx.Graph()
        new_G.add_nodes_from(self.G.nodes)

        q = [(x[2]["weight"], x) for x in self.G.edges(data=True)]
        heapq.heapify(q)
        while q:
            _, (f, t, _) = heapq.heappop(q)
            if networkx.has_path(new_G, f, t):
                # Same component already
                continue

            new_G.add_edge(f, t)
            if networkx.is_connected(new_G):
                return f[0] * t[0]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 40 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 25272 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
