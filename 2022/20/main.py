from collections import defaultdict
import copy
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
        self.filename = "testinput.txt" if self.test else "input.txt"

    def get_data(self, key):
        self.original = list(
            enumerate(
                int(line) * key
                for line in open(self.filename).read().rstrip().split("\n")
            )
        )
        self.data = copy.copy(self.original)

    def run(self, mix_count=1, key=1):
        self.get_data(key)
        for _ in range(mix_count):
            for number in self.original:
                i = self.data.index(number)
                new_index = (i + number[1]) % (len(self.data) - 1)
                self.data.insert(new_index, self.data.pop(i))

        for k, v in self.data:
            if v == 0:
                zero_index = self.data.index((k, v))
                self.data = self.data[zero_index:] + self.data[:zero_index]
                return sum(self.data[i * 1000 % len(self.data)][1] for i in range(1, 4))

    def part1(self):
        return self.run()

    def part2(self):
        return self.run(10, 811589153)


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
