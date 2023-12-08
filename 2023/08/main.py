import itertools
import math
import re
import time


def parseLine(line):
    return list(re.findall(r"\w+", line))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.dirs, m = open(filename).read().rstrip().split("\n\n")

        self.data = {}
        for key, *vals in (parseLine(line) for line in m.split("\n")):
            self.data[key] = tuple(vals)

    def length(self, node):
        for i in itertools.count(0):
            d = self.dirs[i % len(self.dirs)]
            if d == "L":
                node = self.data[node][0]
            elif d == "R":
                node = self.data[node][1]
            if node[-1] == "Z":
                return i + 1

    def part1(self):
        return self.length("AAA") if not self.test else self.length("11A")

    def part2(self):
        return math.lcm(
            *(self.length(node) for node in self.data.keys() if node[-1] == "A")
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
