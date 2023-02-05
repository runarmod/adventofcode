import functools
import itertools
import os
import re
import string
import sys
from collections import defaultdict, deque
from pprint import pprint

sys.path.insert(0, "../../")
from utils.util import copy_answer, request_submit, write_solution


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            list(map(int, list(line))) for line in open(filename).read().rstrip().split("\n")
        ]
        self.lowPoints = set()

    def bound(self, x, length):
        return max(0, min(x, length - 1))

    def low_point(self, x_in, y_in):
        x_s = {self.bound(a, len(self.data[0])) for a in {x_in - 1, x_in, x_in + 1}}
        y_s = {self.bound(a, len(self.data)) for a in {y_in - 1, y_in, y_in + 1}}
        return all(
            x_in == a and y_in == b or self.data[y_in][x_in] < self.data[b][a]
            for a, b in itertools.product(x_s, y_s)
        )

    def part1(self):
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if self.low_point(x, y):
                    self.lowPoints.add((x, y))

        return sum(self.data[y][x] + 1 for x, y in self.lowPoints)

    def basin_size(self, x_in, y_in):
        size = 0
        visited = set()
        queue = deque([(x_in, y_in, self.data[y_in][x_in])])
        while queue:
            x, y, height = queue.popleft()
            if (x, y) in visited:
                continue
            if height >= 9:
                continue
            visited.add((x, y))
            size += 1
            for a, b in {
                (self.bound(x - 1, len(self.data[0])), self.bound(y, len(self.data))),
                (self.bound(x + 1, len(self.data[0])), self.bound(y, len(self.data))),
                (self.bound(x, len(self.data[0])), self.bound(y - 1, len(self.data))),
                (self.bound(x, len(self.data[0])), self.bound(y + 1, len(self.data))),
            }:
                if (a, b) not in visited and self.data[b][a] > height:
                    queue.append((a, b, self.data[b][a]))
        return size

    def part2(self):
        return functools.reduce(
            lambda a, b: a * b, sorted([self.basin_size(x, y) for x, y in self.lowPoints])[-3:]
        )


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
