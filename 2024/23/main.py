import time

import networkx
from aoc_utils_runarmod import get_data


def parseLine(line):
    return line.split("-")


def parseLines(lines):
    return [parseLine(line) for line in lines]


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(2024, 23, test=test).strip("\n").split("\n")
        data = parseLines(data)

        self.G = networkx.Graph()
        self.G.add_edges_from(data)

    def part1(self):
        return sum(
            any(node[0] == "t" for node in clique)
            for clique in networkx.enumerate_all_cliques(self.G)
            if len(clique) == 3
        )

    def part2(self):
        return ",".join(sorted(max(networkx.enumerate_all_cliques(self.G), key=len)))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 7 else 'wrong :('}")
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 'co,de,ka,ta' else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
