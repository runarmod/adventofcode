import itertools
import time

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = list(
            map(list, get_data(2025, 4, test=test).strip("\n").split("\n"))
        )

    def get_removable(self, grid: list[list[str]]) -> list[tuple[int, int]]:
        removable = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if not grid[y][x] == "@":
                    continue
                b = 0
                for nx, ny in neighbors8((x, y)):
                    if not (nx in range(len(grid[0])) and ny in range(len(grid))):
                        continue
                    if grid[ny][nx] == "@":
                        b += 1
                if b < 4:
                    removable.append((x, y))
        return removable

    def part1(self):
        return len(self.get_removable(self.data))

    def part2(self):
        s = 0
        while True:
            removable = self.get_removable(self.data)
            if not removable:
                break
            s += len(removable)
            for x, y in removable:
                self.data[y][x] = "."
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 13 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 43 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


def neighbors8(point: tuple[int, ...], jump=1):
    for diff in itertools.product((-jump, 0, jump), repeat=len(point)):
        if any(diff):
            yield tuple(point[i] + diff[i] for i in range(len(point)))


if __name__ == "__main__":
    main()
