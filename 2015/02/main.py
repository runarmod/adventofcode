import re
import time
from itertools import permutations


def parseLine(line):
    return list(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def area(self, x, y, z):
        return sum(a * b for a, b in permutations((x, y, z), r=2))

    def volume(self, x, y, z):
        return x * y * z

    def smallest_side(self, x, y, z):
        return min(x * y, y * z, x * z)

    def part1(self):
        return sum(self.area(*side) + self.smallest_side(*side) for side in self.data)

    def part2(self):
        return sum(
            self.volume(*side) + 2 * self.smallest_side(*side) for side in self.data
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 58 + 43 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 34 + 14 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
