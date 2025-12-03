import functools
import time

from aoc_utils_runarmod import get_data


@functools.lru_cache(maxsize=None)
def largest_number(numbers, count):
    if count == 0 or not numbers:
        return 0
    if len(numbers) == count:
        return sum(n * 10**i for i, n in enumerate(reversed(numbers)))
    remaining_nums = tuple(numbers[1:])
    return max(
        largest_number(remaining_nums, count),
        largest_number(remaining_nums, count - 1) + numbers[0] * 10 ** (count - 1),
    )


class Solution:
    def __init__(self, test=False):
        self.test = test

        self.data = [
            tuple(int(c) for c in line)
            for line in get_data(2025, 3, test=test).strip("\n").split("\n")
        ]

    def solve(self, count):
        return sum(largest_number(line, count) for line in self.data)

    def part1(self):
        return self.solve(2)

    def part2(self):
        return self.solve(12)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 357 else 'wrong :('}")
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 3121910778619 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
