import time
from functools import cache

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 19) if not self.test else open("testinput.txt").read())
            .strip("\n")
            .split("\n\n")
        )

        self.patterns = data[0].split(", ")
        self.designs = data[1].split("\n")

    def works(self, word: str):
        if len(word) == 0:
            return True

        return any(
            word.startswith(rule) and self.works(word[len(rule) :])
            for rule in self.patterns
        )

    def part1(self):
        return sum(map(self.works, self.designs))

    @cache
    def count(self, word: str):
        if len(word) == 0:
            return 1
        return sum(
            self.count(word[len(p) :]) for p in self.patterns if word.startswith(p)
        )

    def part2(self):
        return sum(map(self.count, self.designs))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 6 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 16 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
