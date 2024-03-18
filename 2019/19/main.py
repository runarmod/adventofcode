import itertools
import time

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = [int(line) for line in open("input.txt").read().rstrip().split(",")]

    def check(self, x, y):
        self.computer = IntcodeComputer(self.data)
        self.computer.input(x)
        self.computer.input(y)
        return self.computer.run() == 1

    def part1(self):
        return sum(self.check(x, y) for x, y in itertools.product(range(50), repeat=2))

    def part2(self):
        x = 0
        for y in itertools.count(99):
            while not self.check(x, y):
                x += 1
            if self.check(x + 99, y - 99):
                return x * 10000 + y - 99


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
