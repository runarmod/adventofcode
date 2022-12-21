from collections import defaultdict
from pprint import pprint
import itertools
import pyperclip
import re
import string

from tqdm import trange


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.instructions = open(filename).read().rstrip()
        self.shapes = [
            "####".split("\n"),
            ".#.\n###\n.#.".split("\n"),
            "..#\n..#\n###".split("\n"),
            "#\n#\n#\n#".split("\n"),
            "##\n##".split("\n"),
        ]

    def move_left(self, shape, l, fall_distance):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == "#":
                    if j == 0 or shape[i][j - 1] != "#":
                        if self.diagram[i + fall_distance][j + l - 1] == "#":
                            return False
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == "#":
                    self.diagram[i + fall_distance][j + l - 1] = "#"
                    self.diagram[i + fall_distance][j + l] = "."
        return True

    def move_right(self, shape, l, fall_distance):
        for i in range(len(shape)):
            for j in range(len(shape[0]) - 1, -1, -1):
                if shape[i][j] == "#":
                    if j == len(shape[i]) - 1 or shape[i][j + 1] != "#":
                        if self.diagram[i + fall_distance][j + l + 1] == "#":
                            return False
        for i in range(len(shape)):
            for j in range(len(shape[0]) - 1, -1, -1):
                if shape[i][j] == "#":
                    self.diagram[i + fall_distance][j + l + 1] = "#"
                    self.diagram[i + fall_distance][j + l] = "."
        return True

    def move_down(self, shape, l, fall_distance):
        for i in range(len(shape) - 1, -1, -1):
            for j in range(len(shape[i])):
                if shape[i][j] == "#":
                    if i == len(shape) - 1 or shape[i + 1][j] != "#":
                        if self.diagram[i + fall_distance + 1][j + l] == "#":
                            return False
        for i in range(len(shape) - 1, -1, -1):
            for j in range(len(shape[i])):
                if shape[i][j] == "#":
                    self.diagram[i + fall_distance + 1][j + l] = "#"
                    self.diagram[i + fall_distance][j + l] = "."
        return True

    def extend_diagram(self):
        for i in range(len(self.diagram)):
            if self.diagram[i].count("#"):
                break
        if i < 2:
            while i < 2:
                self.diagram = [["." for _ in range(7)]] + self.diagram
                i += 1
        elif i > 3:
            while i > 3:
                self.diagram = self.diagram[1:]
                i -= 1

    def add_shape(self, shape):
        new_shape = []
        for i in range(len(shape)):
            new_shape.append(
                ["." for _ in range(2)]
                + list(shape[i])
                + ["." for _ in range(7 - len(shape[i]) - 2)]
            )

        self.diagram = new_shape + self.diagram

    def part1(self):
        return self.run(1)

    def run(self, part):
        self.diagram = [["." for _ in range(7)] for _ in range(3)] + [
            ["#" for _ in range(7)]
        ]
        instruction_index = -1
        shape_index = -1

        for num in trange(2022 if part == 1 else 1000000000000):
            if num % 10 == 0:
                self.diagram = self.diagram[:20]
            shape_index = (shape_index + 1) % len(self.shapes)
            shape = self.shapes[shape_index]
            l = 2
            # r = len(shape[0]) + l - 1
            fall_distance = -1
            self.extend_diagram()
            self.add_shape(self.shapes[shape_index])
            while True:
                fall_distance += 1
                instruction_index = (instruction_index + 1) % len(self.instructions)
                direction = self.instructions[instruction_index]
                if direction == "<":
                    if l > 0:
                        l -= self.move_left(shape, l, fall_distance)
                elif direction == ">":
                    if l + len(shape[0]) - 1 < 6:
                        l += self.move_right(shape, l, fall_distance)
                if not self.move_down(shape, l, fall_distance):
                    break
        # pprint(self.diagram)
        self.extend_diagram()
        return len(self.diagram) - 1 - 3

    def part2(self):
        return self.run(2)


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
