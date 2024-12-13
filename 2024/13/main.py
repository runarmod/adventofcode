import re
import time

from aoc_utils_runarmod import get_data


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 13) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n\n")
        )

        self.data = []
        for section in data:
            s = []
            for line in section.split("\n"):
                s.append(parseNumbers(line))
            self.data.append(s)

    def run(self, prize_func=lambda x: x):
        s = 0
        for machine in self.data:
            (A0, A1), (B0, B1), prize = machine
            X, Y = map(prize_func, prize)
            a = (B1 * X - B0 * Y) / (A0 * B1 - A1 * B0)
            b = (A0 * Y - A1 * X) / (A0 * B1 - A1 * B0)
            if all(abs(c - round(c)) < 1e-7 for c in (a, b)):
                s += round(a) * 3 + round(b)
        return s

    def part1(self):
        return self.run()

    def part2(self):
        return self.run(prize_func=lambda x: x + 10**13)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 480 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
