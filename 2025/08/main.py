import functools
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
                weight=(
                    ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
                    ** 0.5
                ),
            )

    def part1(self):
        new_G = networkx.Graph()
        for edge in sorted(self.G.edges(data=True), key=lambda x: x[2]["weight"])[
            : (1000 if not self.test else 10)
        ]:
            new_G.add_edge(edge[0], edge[1], weight=edge[2]["weight"])

        largest_components = sorted(
            networkx.connected_components(new_G), key=len, reverse=True
        )[:3]
        return functools.reduce(lambda x, y: x * y, map(len, largest_components))

    def part2(self):
        new_G = networkx.Graph()
        new_G.add_nodes_from(self.G.nodes)

        for edge in sorted(self.G.edges(data=True), key=lambda x: x[2]["weight"]):
            if networkx.has_path(new_G, edge[0], edge[1]):
                # Same component already
                continue

            new_G.add_edge(edge[0], edge[1], weight=edge[2]["weight"])
            if networkx.is_connected(new_G):
                return edge[0][0] * edge[1][0]


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
