from itertools import permutations
from math import inf
import re
from typing import List
from collections import defaultdict


class Solution():
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        # self.data = open(filename).read().rstrip().split("\n")
        self.pattern = re.compile(r"(\w+) to (\w+) = (\d+)")
        self.matches = [(start, end, int(distance)) for start, end,
                        distance in self.pattern.findall(open(filename).read())]
        self.places = set()

        self.generateDistanceMap()
        self.generateDistancePermutation()

    def generateDistanceMap(self):
        self.dict = defaultdict(dict)
        for start, end, distance in self.matches:
            self.places.add(start)
            self.places.add(end)
            self.dict[start][end] = distance
            self.dict[end][start] = distance

    def generateDistancePermutation(self):
        self.distances = [sum(map(lambda x, y: self.dict[x][y], perm[:-1], perm[1:]))
                          for perm in permutations(self.places)]

    def part1(self):
        return min(self.distances)

    def part2(self):
        return max(self.distances)


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
