import functools
import re
import time
from typing import Literal

import numpy as np
from aoc_utils_runarmod import get_data


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def numsNested(
    data: str | list[str] | list[list[str]],
) -> tuple[int | tuple[int, ...], ...]:
    if isinstance(data, str):
        return nums(data)
    if not hasattr(data, "__iter__"):
        raise ValueError("Data must be a tuple/list/iterable or a string")
    return tuple(e[0] if len(e) == 1 else e for e in filter(len, map(numsNested, data)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(2025, 6, test=test).strip("\n").split("\n")
        self.og_data = data

        self.numbers_lines = numsNested(data)
        self.math = re.findall(r"[\+\*]", data[-1])

    def math_nums(self, numbers: list[int], operation: Literal["+", "*"]) -> int:
        if operation == "+":
            return sum(numbers)
        return functools.reduce(lambda x, y: x * y, numbers)

    def part1(self):
        transposed = list(zip(*self.numbers_lines))
        return sum(
            self.math_nums(transposed[i], self.math[i]) for i in range(len(self.math))
        )

    def part2(self):
        s = 0
        first_is = [i for i, c in enumerate(self.og_data[-1]) if c != " "]
        array = np.array([list(line) for line in self.og_data][:-1])

        for i in range(len(self.math)):
            sub_array = array[
                :, first_is[i] : first_is[i + 1] - 1 if i + 1 < len(first_is) else None
            ]
            transposed = sub_array.T.tolist()
            reversed_transposed = [list(reversed(row)) for row in transposed]
            numbers = list(
                map(int, ["".join(reversed(row)) for row in reversed_transposed])
            )

            s += self.math_nums(numbers, self.math[i])

        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 4277556 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 3263827 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
