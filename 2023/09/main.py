import re
import time


def parseLine(line):
    return list(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def go_down(self, line):
        l = [line[:]]
        while not all(l[-1][i] == 0 for i in range(len(l[-1]))):
            nl = []
            for i in range(len(l[-1]) - 1):
                nl.append(l[-1][i + 1] - l[-1][i])
            l.append(nl)
        return l

    def part1(self):
        s = 0
        for line in self.data:
            l = self.go_down(line)

            l[-1].append(0)
            for i in range(len(l) - 2, -1, -1):
                l[i].append(l[i][-1] + l[i + 1][-1])
            s += l[0][-1]
        return s

    def part2(self):
        s = 0
        for line in self.data:
            l = self.go_down(line)

            l[-1].insert(0, 0)
            for i in range(len(l) - 2, -1, -1):
                l[i].insert(0, l[i][0] - l[i + 1][0])
            s += l[0][0]
        return s


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
