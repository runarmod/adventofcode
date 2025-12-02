import itertools
import re
import time

from aoc_utils_runarmod import get_data


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(2025, 2, test=test).strip("\n")

        self.data = [range(f, t + 1) for f, t in itertools.batched(nums(data), 2)]

    def invalid(self, ID: int, part: int) -> bool:
        return re.match(r"^(.+)\1+$" if part == 2 else r"^(.+)\1$", str(ID)) is not None

    def solve(self, part: int):
        s = 0
        for r in self.data:
            for ID in r:
                if self.invalid(ID, part):
                    s += ID
        return s

    def part1(self):
        return self.solve(1)

    def part2(self):
        return self.solve(2)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 1227775554 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 4174379265 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
