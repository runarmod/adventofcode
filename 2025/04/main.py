import itertools
import time

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = set(
            (x, y)
            for y, line in enumerate(
                get_data(2025, 4, test=test).strip("\n").split("\n")
            )
            for x, char in enumerate(line)
            if char == "@"
        )

    def get_removable(self, rolls: set[tuple[int, int]]) -> set[tuple[int, int]]:
        return {
            pos for pos in rolls if sum(n_pos in rolls for n_pos in neighbors8(pos)) < 4
        }

    def part1(self):
        return len(self.get_removable(self.data))

    def part2(self):
        s = 0
        removable = set()
        while removable or s == 0:
            removable = self.get_removable(self.data)
            s += len(removable)
            self.data -= removable
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
