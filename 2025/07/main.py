import functools
import itertools
import time

from aoc_utils_runarmod import get_data


def get_first_position(grid: list[list[int]], target: int) -> tuple[int, int] | None:
    w, h = len(grid[0]), len(grid)

    for x, y in itertools.product(range(w), range(h)):
        if grid[y][x] == target:
            return (x, y)
    return None


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = get_data(2025, 7, test=test).strip("\n").split("\n")

    def part1(self):
        counter = 0
        beams = {get_first_position(self.data, "S")}

        while len(beams):
            next_beams = set()
            for beam in beams:
                if beam[1] + 1 >= len(self.data):
                    continue
                elif self.data[beam[1] + 1][beam[0]] == ".":
                    next_beams.add((beam[0], beam[1] + 1))
                elif self.data[beam[1] + 1][beam[0]] == "^":
                    counter += 1
                    next_beams.add((beam[0] - 1, beam[1] + 1))
                    next_beams.add((beam[0] + 1, beam[1] + 1))
            beams = next_beams
        return counter

    @functools.cache
    def get_path_count(self, x, y):
        if y + 1 >= len(self.data):
            return 1
        if self.data[y + 1][x] == "^":
            return self.get_path_count(x + 1, y + 1) + self.get_path_count(x - 1, y + 1)
        return self.get_path_count(x, y + 1)

    def part2(self):
        return self.get_path_count(*get_first_position(self.data, "S"))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 21 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 40 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
