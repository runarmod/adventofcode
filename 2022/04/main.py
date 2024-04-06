from collections import defaultdict
import itertools
import re
import string


def parseLine(line):
    return tuple(map(int, re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", line)[0]))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        return sum(
            line[0] >= line[2]
            and line[1] <= line[3]
            or line[0] <= line[2]
            and line[1] >= line[3]
            for line in self.data
        )

    def part2(self):
        return sum(
            bool(
                set(range(line[0], line[1] + 1)).intersection(
                    set(range(line[2], line[3] + 1))
                )
            )
            for line in self.data
        )


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
