import functools
import itertools
import os
import re
import string
import sys
import time
from collections import defaultdict, deque
from pprint import pprint

sys.path.insert(0, "../../")
from utils import copy_answer, request_submit, write_solution


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [int(x) for x in open(filename).read().rstrip()]
        self.pattern = [0, 1, 0, -1]

    def get_pattern(self, idx):
        first = True
        for i in itertools.count():
            for j in range(idx + 1):
                if first and j == 0:
                    first = False
                    continue
                yield self.pattern[i % len(self.pattern)]

    def part1(self):
        nums = self.data
        for _ in range(100):
            new_nums = []
            for digit_index in range(len(nums)):
                s = 0
                for digit_pattern, digit_input in zip(
                    itertools.islice(self.get_pattern(digit_index), len(nums)), nums
                ):
                    s += digit_input * digit_pattern
                new_nums.append(abs(s) % 10)
            nums = new_nums
        return int("".join(map(str, nums[:8])))

    def part2(self):
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 52432133 else 'wrong :('}"
    )
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == None else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit(2019, 16, part1, part2)


if __name__ == "__main__":
    main()
