import time
from collections import Counter

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(2025, 1, test=test).strip("\n")

        self.data = [(line[0], int(line[1:])) for line in data.split("\n")]

    def part1(self):
        c = 50
        times = Counter()
        for direction, distance in self.data:
            if direction == "R":
                c += distance
            elif direction == "L":
                c -= distance
            c %= 100
            times[c] += 1
        return times.most_common(1)[0][1]

    def part2(self):
        c = 50
        times = Counter()
        for direction, distance in self.data:
            for _ in range(distance):
                if direction == "R":
                    c += 1
                elif direction == "L":
                    c -= 1
                c %= 100
                times[c] += 1
        return times[0]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 3 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 6 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
