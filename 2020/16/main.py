import functools
import itertools
import re
import time
from collections import defaultdict


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        type, your, nearby = open(filename).read().rstrip().split("\n\n")

        self.type = [
            [range(line[i], line[i + 1] + 1) for i in range(0, len(line), 2)]
            for line in [
                list(map(int, re.findall(r"\d+", line))) for line in type.split("\n")
            ]
        ]

        self.your = list(map(int, your.split("\n")[1].split(",")))

        self.nearby = [
            list(map(int, line.split(","))) for line in nearby.split("\n")[1:]
        ]

    def part1(self):
        s = 0
        for line in self.nearby:
            for num in line:
                if not any(num in r for r in itertools.chain(*self.type)):
                    s += num
        return s

    def part2(self):
        for i in range(len(self.nearby) - 1, -1, -1):
            for num in self.nearby[i]:
                if not any(num in r for r in itertools.chain(*self.type)):
                    self.nearby.pop(i)
                    break

        fixed: dict[int, int] = {}  # type_id: col_id

        while len(fixed) < len(self.type):
            possible: dict[int, set[int]] = defaultdict(set)  # type_id: set(col_id)
            for i in range(len(self.type)):
                for j in range(len(self.your)):
                    if (
                        all(
                            any(num in r for r in self.type[i])
                            for num in [line[j] for line in self.nearby]
                        )
                        and j not in fixed.values()
                    ):
                        possible[i].add(j)
            for i in range(len(self.type)):
                if len(possible[i]) == 1:
                    fixed[i] = possible[i].pop()
                    for j in range(len(self.type)):
                        possible[j].discard(fixed[i])
        return functools.reduce(
            lambda x, y: x * y, [self.your[fixed[i]] for i in range(6)]
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 71 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
