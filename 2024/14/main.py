import functools
import itertools
import re
import time
from collections import defaultdict

from aoc_utils_runarmod import get_data


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        lines = (
            (get_data(2024, 14) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )

        self.data = list(map(parseNumbers, lines))
        self.R = 103
        self.C = 101
        if self.test:
            self.C = 11
            self.R = 7

    def iterate(self, data):
        d = data[:]
        for _ in itertools.count():
            for i, (px, py, vx, vy) in enumerate(d):
                d[i] = ((px + vx) % self.C, (py + vy) % self.R, vx, vy)
            yield d

    def part1(self):
        data = next(itertools.islice(self.iterate(self.data), 100, 101))

        quadrants = defaultdict(int)
        half_R = self.R // 2
        half_C = self.C // 2
        for px, py, _, _ in data:
            if px == half_C or py == half_R:
                continue
            quadrants[px < half_C, py < half_R] += 1

        return functools.reduce(lambda x, y: x * y, quadrants.values(), 1)

    def dfs(self, s, node_x, node_y, depth):
        if depth == 0:
            return True
        if (node_x + 1, node_y) not in s:
            return False

        return self.dfs(s, node_x + 1, node_y, depth - 1)

    def part2(self):
        for iteration, data in enumerate(self.iterate(self.data), start=1):
            s = {(px, py) for px, py, _, _ in data}
            for px, py in s:
                if self.dfs(s, px, py, 10):
                    return iteration


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 12 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
