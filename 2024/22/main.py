import re
import time
from collections import Counter, deque

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
        data = (
            (get_data(2024, 22) if not self.test else open("testinput.txt").read())
            .strip("\n")
            .split("\n")
        )

        self.data = numsNested(data)

    def secret(self, num, iterations):
        prev_price = num % 10
        price_diffs = deque(maxlen=4)
        d = {}

        for _ in range(iterations):
            num = ((num * 64) ^ num) % 16777216
            num = ((num // 32) ^ num) % 16777216
            num = ((num * 2048) ^ num) % 16777216

            price = num % 10
            diff = price - prev_price
            price_diffs.append(diff)
            tuple_diffs = tuple(price_diffs)
            if len(price_diffs) == 4 and tuple_diffs not in d:
                d[tuple_diffs] = price
            prev_price = price
        return num, d

    def part1(self):
        return sum(self.secret(num, 2000)[0] for num in self.data)

    def part2(self):
        ds = Counter()
        for num in self.data:
            ds.update(self.secret(num, 2000)[1])
        return ds.most_common(1)[0][1]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, {'correct :)' if test1 == 37990510 else 'wrong :('}"
    )
    print(f"(TEST) Part 2: {test2}, {'correct :)' if test2 == 23 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
