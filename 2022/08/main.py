from collections import defaultdict
import itertools
import re
import string
from pprint import pprint


def parseLine(line):
    return list(map(int, list(line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        s = len(self.data) * 2 + len(self.data[0]) * 2 - 4
        for i in range(1, len(self.data) - 1):
            for j in range(1, len(self.data[i]) - 1):
                if self.check(i, j):
                    s += 1
        return s

    def check(self, i, j):
        for x in (-1, 1):
            flag = True
            mul = 1
            while 0 <= i + x * mul < len(self.data):
                if self.data[i][j] <= self.data[i + x * mul][j]:
                    flag = False
                    break
                mul += 1
            if flag:
                # print(f"{i=}, {j=}, {self.data[i][j]=}, {i+x*mul=}")
                return True
        for y in (-1, 1):
            flag = True
            mul = 1
            while 0 <= j + y * mul < len(self.data[0]):
                if self.data[i][j] <= self.data[i][j + y * mul]:
                    flag = False
                    break
                mul += 1
            if flag:
                # print(f"{i=}, {j=}, {self.data[i][j]=}, {j+y*mul=}")
                return True
        return False
    
    def scienic_score(self, i, j):
        m = 1
        for x in (-1, 1):
            # s = 0
            mul = 1
            while 0 <= i + x * mul < len(self.data):
                if self.data[i][j] <= self.data[i + x * mul][j]:
                    m *= mul
                    break
                # s += 1
                mul += 1
            else:
                m *= mul - 1
        for y in (-1, 1):
            # s = 0
            mul = 1
            while 0 <= j + y * mul < len(self.data):
                if self.data[i][j] <= self.data[i][j + y * mul]:
                    m *= mul
                    break
                # s += 1
                mul += 1
            else:
                m *= mul - 1
        return m

    def scienic_scores(self):
        for i in range(1, len(self.data) - 1):
            for j in range(1, len(self.data[i]) - 1):
                yield self.scienic_score(i, j)

    def part2(self):
        # print(list(self.scienic_scores()))
        return max(self.scienic_scores())


def main():
    test = Solution(test=True)
    print(part1_test := f"(TEST) Part 1: {test.part1()}")
    print(part2_test := f"(TEST) Part 2: {test.part2()}")
    # return
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
