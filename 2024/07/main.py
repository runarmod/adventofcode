import re
import time

from aoc_utils_runarmod import get_data


def parseLines(lines):
    return [parseNumbers(line) for line in lines]


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 7) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )

        self.data = parseLines(data)

    def can_be_true(self, answer, nums, part2=False):
        if len(nums) == 1:
            return nums[0] == answer

        a, b, rest = nums[0], nums[1], nums[2:]

        return (
            self.can_be_true(answer, [a + b] + rest, part2)
            or self.can_be_true(answer, [a * b] + rest, part2)
            or (
                part2 and self.can_be_true(answer, [int(str(a) + str(b))] + rest, part2)
            )
        )

    def run(self, part2=False):
        return sum(
            answer
            for answer, *nums in self.data
            if self.can_be_true(answer, nums, part2)
        )

    def part1(self):
        return self.run()

    def part2(self):
        return self.run(part2=True)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 3749 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 11387 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
