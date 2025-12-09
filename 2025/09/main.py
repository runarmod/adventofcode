import re
import time

import shapely
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
        self.data = get_data(2025, 9, test=test).strip("\n").split("\n")
        self.data = numsNested(self.data)

    def rect_area(self, p1, p2):
        return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

    def part1(self):
        best = 0
        for i in range(len(self.data) - 1):
            for j in range(i + 1, len(self.data)):
                best = max(
                    best,
                    self.rect_area(self.data[i], self.data[j]),
                )
        return best

    def part2(self):
        perimeter = list(self.data) + [self.data[0]]

        poly = shapely.Polygon(perimeter)
        shapely.prepare(poly)
        best_area = 0

        for i in range(len(perimeter) - 1):
            for j in range(i + 1, len(perimeter)):
                area = self.rect_area(perimeter[i], perimeter[j])
                if area <= best_area:
                    continue

                if poly.covers(shapely.box(*perimeter[i], *perimeter[j])):
                    best_area = area

        return int(best_area)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 50 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 24 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
