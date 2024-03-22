import os
import time

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))
        self.computer = IntcodeComputer(self.data)

    def part1(self):
        program = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK"""
        self.computer.inputs = list(map(ord, program + "\n"))
        for a in self.computer.iter():
            try:
                print(chr(a), end="")
            except ValueError:
                return int(a)
        return None

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
