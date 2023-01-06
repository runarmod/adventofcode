import os
import string
import sys

sys.path.insert(0, "../../")
from utils.util import copy_answer, write_solution


class Solution:
    def __init__(self):
        filename = "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split("-")))

    def generate_passwords(self, part):
        for i in range(self.data[0], self.data[1]):
            s = str(i)
            if s != "".join(sorted(s)):
                continue
            if len(s) <= len(set(s)):
                continue
            if part == 2 and not any(s.count(d) == 2 for d in string.digits):
                continue
            yield i

    def part1(self):
        return len(list(self.generate_passwords(part=1)))

    def part2(self):
        return len(list(self.generate_passwords(part=2)))


def main():
    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    # copy_answer(part1, part2)
    # write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)


if __name__ == "__main__":
    main()
