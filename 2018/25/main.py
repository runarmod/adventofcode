import itertools
import time

import networkx as nx


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = {
            tuple(map(int, line.split(","))) for line in open(filename).read().rstrip().split("\n")
        }

    def manhattan(self, a, b):
        return sum(abs(x - y) for x, y in zip(a, b))

    def part1(self):
        G = nx.Graph()
        G.add_edges_from(
            (u, v)
            for u, v in itertools.combinations_with_replacement(self.data, 2)
            if self.manhattan(u, v) <= 3
        )
        return nx.number_connected_components(G)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
