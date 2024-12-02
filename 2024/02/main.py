import re
import time

from more_itertools import mark_ends


def parseLines(lines):
    return [parseNumbers(line) for line in lines]


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        with open(filename) as f:
            data = f.read().rstrip()

        self.data = parseLines(data.split("\n"))

    def safe(self, line):
        inc = 0
        prev = None
        for first, _, num in mark_ends(line):
            if first:
                prev = num
                inc = line[1] > line[0]
                continue
            if abs(prev - num) not in range(1, 4):
                return 0
            if inc and num <= prev:
                return 0
            if not inc and num >= prev:
                return 0
            prev = num
        else:
            return 1

    def part1(self):
        return sum(map(self.safe, self.data))

    def part2(self):
        s = 0
        for line in self.data:
            safe = self.safe(line)
            if safe:
                s += 1
                continue
            if not safe:
                for i in range(len(line)):
                    if self.safe(line[:i] + line[i + 1 :]):
                        s += 1
                        break
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 2 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 4 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
