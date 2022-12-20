from collections import defaultdict
from functools import cmp_to_key
from pprint import pprint
from itertools import zip_longest
import pyperclip
import re
import string


def parseLine(line):
    return eval(line)


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line)
            for line in open(filename).read().rstrip().replace("\n\n", "\n").split("\n")
        ]

    def compare(self, left, right):
        if left is None:
            return -1
        if right is None:
            return 1

        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1
            elif left == right:
                return 0
            else:
                return 1
        if isinstance(left, list) and isinstance(right, list):
            for l1, r1 in zip_longest(left, right):
                if (c := self.compare(l1, r1)) != 0:
                    return c
            return 0
        l = [left] if isinstance(left, int) else left
        r = [right] if isinstance(right, int) else right
        return self.compare(l, r)

    def part1(self):
        s = 0
        for i in range(0, len(self.data), 2):
            left, right = self.data[i], self.data[i + 1]
            if self.compare(left, right) == -1:
                s += i // 2 + 1
        return s

    def part2(self):
        start, end = [[2]], [[6]]
        self.data.extend([start, end])
        self.data.sort(key=cmp_to_key(self.compare))
        return (self.data.index(start) + 1) * (self.data.index(end) + 1)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    copy_answer(part1, part2)

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


def copy_answer(part1, part2):
    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)


if __name__ == "__main__":
    main()
