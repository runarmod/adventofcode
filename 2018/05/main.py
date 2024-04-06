from collections import defaultdict
import itertools
import re
import string


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()

    def part1(self):
        return self.find_final_length(self.data)

    def find_final_length(self, data):
        keep_going = True
        while keep_going:
            keep_going = False
            for c in string.ascii_lowercase:
                tests = (c + c.upper(), c.upper() + c)
                for test in tests:
                    if test in data:
                        keep_going = True
                        data = data.replace(test, "")
        return len(data)

    def part2_help(self):
        for c in string.ascii_lowercase:
            data_copy = self.data.replace(c, "").replace(c.upper(), "")
            yield self.find_final_length(data_copy)

    def part2(self):
        return min(self.part2_help())


def main():
    test = Solution(test=True)
    print(part1_test := f"Part 1: {test.part1()}")
    print(part2_test := f"Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
