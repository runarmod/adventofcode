import itertools
import os
import re
import string
import sys
from collections import defaultdict, deque
from pprint import pprint

sys.path.insert(0, "../../")
from utils.util import copy_answer, request_submit, write_solution


def parseLine(line):
    line = line.split(",")
    return (int(line[0]), int(line[1]))


def parseFold(line):
    line = re.split(r"[ =]", line)
    # print(line)
    return (line[-2], int(line[-1]))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.coords = {
            parseLine(line) for line in open(filename).read().rstrip().split("\n\n")[0].split("\n")
        }
        self.folds = (
            parseFold(line) for line in open(filename).read().rstrip().split("\n\n")[1].split("\n")
        )
        self.iter = self.do_folds()

    def new_coord(self, val, fold_index):
        if val < fold_index:
            return val
        return 2 * fold_index - val

    def do_folds(self):
        coords = self.coords.copy()
        for fold in self.folds:
            if fold[0] == "x":
                # First remove on fold
                coords = {(x, y) for x, y in coords if x != fold[1]}

                # Do the folds
                coords = {(self.new_coord(x, fold[1]), y) for x, y in coords}
            else:
                # First remove on fold
                coords = {(x, y) for x, y in coords if y != fold[1]}

                # Do the folds
                coords = {(x, self.new_coord(y, fold[1])) for x, y in coords}
            yield coords

    def part1(self):
        self.coords = next(self.iter)
        return len(self.coords)

    def part2(self):
        for newCoords in self.iter:
            self.coords = newCoords
        for y in range(max(self.coords, key=lambda x: x[1])[1] + 1):
            for x in range(max(self.coords, key=lambda x: x[0])[0] + 1):
                print("█" if (x, y) in self.coords else " ", end="")
            print()
        return "HZLEHJRK"


def main():
    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")
    part2 = solution.part2()
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
