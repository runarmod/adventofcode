import time
from collections import defaultdict
import numpy as np

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = (
            (get_data(2024, 4) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )
        self.word = "XMAS"

    def get_groups(self, rows=True, columns=True, diagonals=True):
        """
        https://stackoverflow.com/a/43311126/10880273
        """

        def groups(data: list[list], func):
            grouping = defaultdict(list)
            for y in range(len(data)):
                for x in range(len(data[y])):
                    grouping[func(x, y)].append(data[y][x])
            return ["".join(a) for a in map(grouping.get, sorted(grouping))]

        if rows:
            yield groups(self.data, lambda x, y: y)
        if columns:
            yield groups(self.data, lambda x, y: x)
        if diagonals:
            yield groups(self.data, lambda x, y: x + y)
            yield groups(self.data, lambda x, y: x - y)

    def part1(self):
        s = 0
        for group in self.get_groups():
            for line in group:
                s += line.count(self.word)
                s += line[::-1].count(self.word)
        return s

    def part2(self):
        word = np.array([["M", ".", "S"], [".", "A", "."], ["M", ".", "S"]])
        s = 0
        for i in range(4):
            matrix = np.rot90(word, k=i)
            for y in range(len(self.data) - len(matrix) + 1):
                for x in range(len(self.data[0]) - len(matrix[0]) + 1):
                    if all(
                        self.data[y + i][x + j] == matrix[i][j]
                        for i in range(len(matrix))
                        for j in range(len(matrix[0]))
                        if matrix[i][j] != "."
                    ):
                        s += 1
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 18 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 9 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
