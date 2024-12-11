import re
import time
from collections import Counter

from aoc_utils_runarmod import get_data


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            get_data(2024, 11) if not self.test else open("testinput.txt").read()
        ).rstrip()

        self.data = parseNumbers(data)

    def run(self, rounds: int):
        nums = Counter(self.data)
        for _ in range(rounds):
            new_nums = Counter()
            for num in nums:
                s = str(num)
                if num == 0:
                    new_nums[1] += nums[num]
                elif len(s) % 2 == 0:
                    left, right = s[: len(s) // 2], s[len(s) // 2 :]
                    new_nums[int(left)] += nums[num]
                    new_nums[int(right)] += nums[num]
                else:
                    new_nums[num * 2024] += nums[num]
            nums = new_nums
        return sum(nums.values())

    def part1(self):
        return self.run(25)

    def part2(self):
        return self.run(75)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 55312 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
