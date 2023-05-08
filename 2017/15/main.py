import functools
import itertools
import os
import re
import string
import sys
from collections import defaultdict, deque
from pprint import pprint

sys.path.insert(0, "../../")
from utils import copy_answer, request_submit, write_solution


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.start_values = tuple(map(int, re.findall(r"\d+", open(filename).read().rstrip())))
        self.A_product, self.B_product = 16807, 48271
        self.mod = 2147483647

    def get_values_part1(self):
        a, b = self.start_values
        while True:
            a *= self.A_product
            a %= self.mod
            b *= self.B_product
            b %= self.mod
            yield a, b

    def a_2(self):
        a = self.start_values[0]
        while True:
            a *= self.A_product
            a %= self.mod
            if a % 4 == 0:
                yield a

    def b_2(self):
        b = self.start_values[1]
        while True:
            b *= self.A_product
            b %= self.mod
            if b % 8 == 0:
                yield b

    def part1(self):
        total = 0
        part1_values = self.get_values_part1()
        for _ in range(40_000_000):
            A, B = next(part1_values)
            if A & 0xFFFF == B & 0xFFFF:
                total += 1
        return total

    def part2(self):
        a = self.a_2()
        b = self.b_2()
        return sum(next(a) & 0xFFFF == next(b) & 0xFFFF for _ in range(5_000_000))


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
