import itertools
import time

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = [int(line) for line in open("input.txt").read().rstrip().split(",")]

    def part1(self):
        s = 0
        for x, y in itertools.product(range(50), repeat=2):
            self.computer = IntcodeComputer(self.data)
            self.computer.input(x)
            self.computer.input(y)
            s += self.computer.run()
        return s

    def part2(self):
        return None


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
