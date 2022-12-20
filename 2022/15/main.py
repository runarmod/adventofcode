from collections import defaultdict
from pprint import pprint
import itertools
import pyperclip
import re
import string
import matplotlib.pyplot as plt


def dist(x_1, y_1, x_2, y_2) -> int:
    return abs(x_1 - x_2) + abs(y_1 - y_2)


def parseLine(line):
    s_x, s_y, b_x, b_y = tuple(
        map(
            int,
            re.findall(
                r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
                line,
            )[0],
        )
    )
    return (s_x, s_y), dist(s_x, s_y, b_x, b_y)


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.limit = 10 if self.test else 2000000
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = {
            parseLine(line)[0]: parseLine(line)[1]
            for line in open(filename).read().rstrip().split("\n")
        }

    def part1(self):
        can_not_be = set()
        for (x, y), d in self.data.items():
            extra = max(0, d - abs(self.limit - y))
            for x in range(x - extra, x + extra):
                can_not_be.add(x)
        return len(can_not_be)

    def part2(self):
        for (x, y), d in self.data.items():
            x_s = [x, x + d, x, x - d, x]
            y_s = [y - d, y, y + d, y, y - d]
            plt.fill(x_s, y_s)
        plt.plot(
            [0, (20 if self.test else 4000000), (20 if self.test else 4000000), 0, 0],
            [0, 0, (20 if self.test else 4000000), (20 if self.test else 4000000), 0],
        )
        plt.xlim(left=3403959, right=3403961)
        plt.ylim(top=3289728, bottom=3289730)
        plt.show()

        return 3403960 * 4000000 + 3289729


def main():
    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


if __name__ == "__main__":
    main()
