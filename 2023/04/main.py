import re
import time


def parseLine(line):
    line = line.split(":")[1].split("|")
    return [list(map(int, re.findall(r"\d+", line[0])))] + [
        list(map(int, re.findall(r"\d+", line[1])))
    ]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        s = 0
        for line in self.data:
            winning = set(line[0])
            c = 0
            for num in line[1]:
                if num in winning:
                    c += 1
            if c != 0:
                s += 2 ** (c - 1)
        return s

    def part2(self):
        copies = [0 for _ in range(len(self.data))]
        for i, line in enumerate(self.data, start=0):
            winning = set(line[0])
            c = 0
            for num in line[1]:
                if num in winning:
                    c += 1
            for j in range(1, c + 1):
                copies[i + j] += 1 + copies[i]
        return sum(copies) + len(self.data)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
