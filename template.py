from collections import defaultdict
from pprint import pprint
import itertools
import pyperclip
import re
import string


def parseLine(line):
    return line


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        return None

    def part2(self):
        return None


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    print(part1_text := f"Part 1: {part1}")
    part2 = solution.part2()
    print(part2_text := f"Part 2: {part2}")

    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


if __name__ == "__main__":
    main()
