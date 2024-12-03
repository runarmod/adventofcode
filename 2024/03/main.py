import re
import time

from aoc_utils_runarmod import get_data


def parseLine(line):
    return tuple(re.findall(r"mul\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)", line))


def parseLines(lines):
    return [parseLine(line) for line in lines]


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = (
            (get_data(2024, 3) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )
        self.data = parseLines(self.data)

    def part1(self):
        s = 0
        for line in self.data:
            for num1, num2, _, _ in line:
                if num1 and num2:
                    s += int(num1) * int(num2)
        return s

    def part2(self):
        s = 0
        curr_do = True
        for line in self.data:
            for num1, num2, do, dont in line:
                if do == "do":
                    curr_do = True
                    continue
                if dont == "don't":
                    curr_do = False
                    continue
                if curr_do:
                    s += int(num1) * int(num2)
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 161 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 48 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
