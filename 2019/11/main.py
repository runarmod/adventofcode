from IntcodeComputer import IntcodeComputer
from collections import defaultdict
import time


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))

    def part1(self):
        grid = defaultdict(int)  # 0 is black, 1 is white
        self.walk_grid(grid)
        return len(grid)

    def part2(self):
        grid = defaultdict(int)  # 0 is black, 1 is white
        self.walk_grid(grid, 1)
        self.print_grid(grid)
        return "ABEKZGFG"

    def walk_grid(self, grid, start_color=0):
        direction = 0 + 1j
        pos = 0 + 0j

        computer = IntcodeComputer(self.data)
        computer.inputs.append(start_color)
        while not computer.halted:
            color = computer.run()
            grid[pos] = color
            out_dir = computer.run()  # 0 is left, 1 is right
            direction *= 1j if out_dir == 0 else -1j
            pos += direction
            computer.inputs.append(grid[pos])

    def print_grid(self, grid):
        for y in range(
            max(int(p.imag) for p in grid), min(int(p.imag) for p in grid) - 1, -1
        ):
            for x in range(
                min(int(p.real) for p in grid), max(int(p.real) for p in grid) + 1
            ):
                print(" " if grid[x + y * 1j] == 0 else "#", end="")
            print()


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
