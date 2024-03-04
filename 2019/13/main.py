from IntcodeComputer import IntcodeComputer
from collections import defaultdict
from enum import Enum
import time


class Item(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))

    def part1(self):
        grid: dict[tuple[int, int], Item] = defaultdict(lambda: Item.EMPTY)
        computer = IntcodeComputer(self.data)
        while not computer.halted:
            x = computer.run()
            y = computer.run()
            tile_id = computer.run()
            if any(v is None for v in (x, y, tile_id)):
                break
            grid[x, y] = Item(tile_id)
        return sum(1 for item in grid.values() if item == Item.BLOCK)

    def part2(self):
        computer = IntcodeComputer(self.data)
        computer.memory[0] = 2

        def find_direction():
            ball_x = next(x for x, y in grid if grid[x, y] == Item.BALL)
            paddle_x = next(x for x, y in grid if grid[x, y] == Item.PADDLE)
            return -1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0

        def input_function():
            # self.print_grid(grid)
            # time.sleep(0.05)
            return find_direction()

        computer.in_function = input_function
        grid: dict[tuple[int, int], Item] = defaultdict(lambda: Item.EMPTY)

        while not computer.halted:
            x = computer.run()
            y = computer.run()
            if x == -1 and y == 0:
                score = computer.run()
                continue

            tile_id = computer.run()
            if tile_id is None:
                break
            grid[x, y] = Item(tile_id)
        return score

    def print_grid(self, grid):
        for y in range(min(y for _, y in grid), max(y for _, y in grid) + 1):
            print(
                "".join(
                    " #=_o"[grid[x, y].value]
                    for x in range(min(x for x, _ in grid), max(x for x, _ in grid) + 1)
                )
            )


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
