import functools
import itertools
import math
import os
import re
import string
import sys
import time
from collections import defaultdict, deque
from pprint import pprint

sys.path.insert(0, "../../")
from utils import copy_answer, request_submit, write_solution


def parseLines(lines):
    return int(re.findall(r"\d+", lines[0])[0]), tuple(map(int, re.findall(r"\d+", lines[1])))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.depth, self.target = parseLines(open(filename).read().rstrip().split("\n"))
        pprint(self.depth)
        pprint(self.target)

    def part1(self):
        grid = [[0 for _ in range(self.target[0] + 1)] for _ in range(self.target[1] + 1)]
        for y in range(self.target[1] + 1):
            grid[y][0] = y * 48271

        for x in range(self.target[0] + 1):
            grid[0][x] = x * 16807

        for y in range(1, self.target[1] + 1):
            for x in range(1, self.target[0] + 1):
                grid[y][x] = (grid[y][x - 1] + self.depth) * (grid[y - 1][x] + self.depth) % math.lcm(20183, 3)

        grid[self.target[1]][self.target[0]] = 0

        for y in range(self.target[1] + 1):
            for x in range(self.target[0] + 1):
                grid[y][x] = (grid[y][x] + self.depth) % 20183 % 3
        
        self.grid = grid

        return sum(sum(row) for row in grid)

    def part2(self):
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit(2018, 22, part1, part2)


if __name__ == "__main__":
    main()
