import itertools
import os
import re
import string
import sys
from collections import defaultdict, deque
from pprint import pprint

sys.path.insert(0, "../../")
from utils.util import copy_answer, request_submit, write_solution


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [list(map(int, line)) for line in open(filename).read().rstrip().split("\n")]
        self.flashes = 0
        self.queue = deque()

    def increase_all(self):
        for y in range(len(self.data)):
            for x in range(len(self.data[y])):
                self.data[y][x] += 1
                if self.data[y][x] == 10:
                    self.queue.append((x, y))

    def bound(self, val, _max):
        return max(0, min(val, _max))

    def get_adjacent(self, x, y):
        return {
            (
                self.bound(
                    x + i,
                    len(self.data[0]) - 1,
                ),
                self.bound(
                    y + j,
                    len(self.data) - 1,
                ),
            )
            for i, j in itertools.product([-1, 0, 1], repeat=2)
            if i != 0 or j != 0
        }

    def flash(self):
        while self.queue:
            x, y = self.queue.popleft()
            # self.flashes += 1
            # self.data[y][x] += 1
            for adj in self.get_adjacent(x, y):
                self.data[adj[1]][adj[0]] += 1
                if self.data[adj[1]][adj[0]] == 10:
                    self.queue.append(adj)

    def reset(self):
        size = len(self.data) * len(self.data[0])
        counter = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] >= 10:
                    self.flashes += 1
                    self.data[i][j] = 0
                    counter += 1
        return size == counter

    def part1(self):
        for i in range(100):
            self.increase_all()
            self.flash()
            self.reset()
            # DEBUG
            # if i < 10 or i % 10 == 9:
            #     print("Iteration", i + 1, "flashes:", self.flashes, "total")
            #     print("\n".join("".join(map(str, s)) for s in self.data))
            #     print()

        return self.flashes

    def part2(self):
        i = 100
        while True:
            i += 1
            self.increase_all()
            self.flash()
            if self.reset():
                return i


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
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit(2021, 11, part1, part2)


if __name__ == "__main__":
    main()
