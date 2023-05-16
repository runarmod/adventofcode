import functools
import itertools
from math import ceil
import time
from tqdm import trange


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.serial_number = int(open(filename).read().rstrip())
        self.grid = [[0 for _ in range(301)] for _ in range(301)]
        self.calculate_powers()

    def calculate_powers(self):
        for y, x in itertools.product(range(1, 301), repeat=2):
            self.grid[y][x] = self.power(x, y)

    def power(self, x, y):
        rackID = x + 10
        power = rackID * y
        power += self.serial_number
        power *= rackID
        power //= 100
        power %= 10
        power -= 5
        return power

    def part1(self):
        best = 0
        best_coord = (-1, -1)
        for y, x in itertools.product(range(1, 301 - 3), range(1, 301 - 3)):
            score = sum(
                self.grid[ny][nx] for ny, nx in itertools.product(range(y, y + 3), range(x, x + 3))
            )
            if score > best:
                best = score
                best_coord = (x, y)
        x, y = best_coord
        return f"{x},{y}"

    def part2(self):
        best = 0
        best_stats = (-1, -1)
        for size in trange(1, 301):
            for y in range(1, 301 - size):
                for x in range(1, 301 - size):
                    score = self.score_rectangle(size, size, x, y)
                    if score > best:
                        best = score
                        best_stats = (x, y, size)
        x, y, size = best_stats
        return f"{x},{y},{size}"

    @functools.lru_cache(maxsize=None)
    def score_rectangle(self, width, height, x, y):
        if width <= 2 or height <= 2:
            return sum(
                self.grid[dy][dx]
                for dx, dy in itertools.product(range(x, x + width), range(y, y + height))
            )
        top_left_width = width // 2
        top_left_height = height // 2

        # Calculate score of each rectangle (being hopefull it is previously calculated and cached)

        return sum(
            (
                self.score_rectangle(top_left_width, top_left_height, x, y),
                self.score_rectangle(
                    top_left_width, height - top_left_height, x, y + top_left_height
                ),
                self.score_rectangle(
                    width - top_left_width, top_left_height, x + top_left_width, y
                ),
                self.score_rectangle(
                    width - top_left_width,
                    height - top_left_height,
                    x + top_left_width,
                    y + top_left_height,
                ),
            )
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
