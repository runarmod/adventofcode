import re
import time

from aoc_utils_runarmod import get_data


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"\d+", line)))


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
        ranges, IDs = get_data(2025, 5, test=test).strip("\n").split("\n\n")
        self.ranges = [range(r[0], r[1] + 1) for r in numsNested(ranges.splitlines())]
        self.IDs = nums(IDs)

    def part1(self):
        return sum(any(num in r for r in self.ranges) for num in self.IDs)

    def part2(self):
        ranges = []
        for r in self.ranges:
            start, end = r.start, r.stop - 1
            new_ranges = []
            for nr in ranges:
                if end < nr.start or start > nr.stop - 1:
                    new_ranges.append(nr)
                else:
                    start = min(start, nr.start)
                    end = max(end, nr.stop - 1)
            new_ranges.append(range(start, end + 1))
            ranges = new_ranges
        return sum(r.stop - r.start for r in ranges)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 3 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 14 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
