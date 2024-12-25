import time
from itertools import product

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = map(
            lambda x: x.split("\n"),
            get_data(2024, 25, test=test).strip("\n").split("\n\n"),
        )

    def part1(self):
        locks, keys = [], []
        for thing in self.data:
            coords = {
                (x, y)
                for x, y in product(range(len(thing[0])), range(len(thing)))
                if thing[y][x] == "#"
            }

            if thing[0][0] == "#":
                locks.append(coords)
            else:
                keys.append(coords)

        return sum(len(key & lock) == 0 for key, lock in product(locks, keys))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, {'correct :)' if test1 == 3 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
