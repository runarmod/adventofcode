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
        return self.find_message_with_length(4)

    def part2(self):
        return self.find_message_with_length(14)

    def find_message_with_length(self, length):
        for i in range(length, len(self.data)):
            if len(set(self.data[i : i + length])) == length:
                return i + length
        raise ValueError("No message found")

def main():
    test = Solution(test=True)
    print(part1_test := f"Part 1: {test.part1()}")
    print(part2_test := f"Part 2: {test.part2()}")

    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
