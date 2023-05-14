import re


def parseLine(line):
    return tuple(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.low_high = sorted(set(map(parseLine, open(filename).read().rstrip().split("\n"))))

    def find_max_range(self, r):
        record = r
        for case in self.low_high:
            if r[0] <= case[0] <= r[1] + 1 and case[1] > r[1]:
                record = max(self.find_max_range(case), record, key=lambda x: x[1])
        return record

    def part1(self):
        return self.find_max_range(self.low_high[0])[1] + 1

    def part2(self):
        count = 0
        next_number = self.find_max_range(self.low_high[0])[1] + 1
        while next_number < 2**32 - 1:
            next_range = next(r for r in self.low_high if r[0] > next_number)
            count += next_range[0] - next_number
            next_number = self.find_max_range(next_range)[1] + 1
        return count


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
