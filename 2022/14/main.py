from collections import defaultdict
from pprint import pprint
from itertools import pairwise
import pyperclip
import re
import string


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.max_y = 0
        self.data = [
            self.parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]
        self.map = [["." for _ in range(1000)] for _ in range(self.max_y + 3)]
        self.generate_structures()

    def parseLine(self, line):
        coords = [tuple(map(int, c.split(","))) for c in line.split(" -> ")]
        self.max_y = max(self.max_y, max(coords, key=lambda x: x[1])[1])
        return coords

    def generate_structures(self, data=None):  # sourcery skip: use-itertools-product
        if data is None:
            data = self.data
        for line in data:
            for a, b in pairwise(line):
                for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                    for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                        self.map[y][x] = "#"
        self.create_map_file()

    def create_map_file(self):
        with open("map.txt", "w") as f:
            for row in self.map:
                f.write("".join(row) + "\n")

    def part1(self):
        return self.run(1)

    def run(self, part):
        sand_count = 0
        while True:
            sand = Sand()
            while sand.move(self.map):
                if part == 1 and sand.get_y() > self.max_y:
                    self.create_map_file()
                    return sand_count
            self.map[sand.get_y()][sand.get_x()] = "o"
            if part == 2 and (sand.get_x(), sand.get_y()) == (500, 0):
                self.create_map_file()
                return sum(row.count("o") for row in self.map)
            sand_count += 1

    def part2(self):
        self.generate_structures([[(0, self.max_y + 2), (999, self.max_y + 2)]])
        self.create_map_file()
        return self.run(2)


class Sand:
    def __init__(self):
        self.x = 500
        self.y = 0

    def move(self, map):
        if map[self.y + 1][self.x] == ".":
            self.y += 1
            return True
        if map[self.y + 1][self.x - 1] == ".":
            self.y += 1
            self.x -= 1
            return True
        if map[self.y + 1][self.x + 1] == ".":
            self.y += 1
            self.x += 1
            return True
        return False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


if __name__ == "__main__":
    main()
