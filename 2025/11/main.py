import functools
import re
import time

import networkx
from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(2025, 11, test=test).strip("\n").split("\n")

        self.G = networkx.DiGraph()
        for line in data:
            f, *ts = re.findall(r"\w+", line)
            self.G.add_edges_from((f, t) for t in ts)

        assert networkx.is_directed_acyclic_graph(self.G)

    def part1(self):
        return self.path_count("you", "out", True, True)

        # Original implementation for part 1:
        # from more_itertools import ilen
        # return ilen(networkx.all_simple_paths(self.G, "you", "out"))

    @functools.lru_cache(None)
    def path_count(
        self, start: str, end: str, dac: bool = False, fft: bool = False
    ) -> int:
        # We have to visit dac and fft at least once
        if start == end:
            return dac and fft

        total = 0
        for neighbor in self.G.successors(start):
            total += self.path_count(
                neighbor, end, dac or neighbor == "dac", fft or neighbor == "fft"
            )
        return total

    def part2(self):
        return self.path_count("svr", "out")


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test2 = test.part2()
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 2 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
