from collections import defaultdict, deque
import itertools
import re
import string


def parseLine(line):
    return list(map(int, re.findall(r"move (\d+) from (\d+) to (\d+)", line)[0]))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def reset(self):
        self.stack = [deque() for _ in range(3 if self.test else 9)]
        if not self.test:
            self.stack[0].extend(["N", "S", "D", "C", "V", "Q", "T"])
            self.stack[1].extend(["M", "F", "V"])
            self.stack[2].extend(["F", "Q", "W", "D", "P", "N", "H", "M"])
            self.stack[3].extend(["D", "Q", "R", "T", "F"])
            self.stack[4].extend(["R", "F", "M", "N", "Q", "H", "V", "B"])
            self.stack[5].extend(["C", "F", "G", "N", "P", "W", "Q"])
            self.stack[6].extend(["W", "F", "R", "L", "C", "T"])
            self.stack[7].extend(["T", "Z", "N", "S"])
            self.stack[8].extend(["M", "S", "D", "J", "R", "Q", "H", "N"])
        else:
            self.stack[0].extend(["Z", "N"])
            self.stack[1].extend(["M", "C", "D"])
            self.stack[2].extend(["P"])

    def part1(self):
        self.reset()
        for num, fra, til in self.data:
            for _ in range(num):
                self.stack[til - 1].append(self.stack[fra - 1].pop())
        return "".join(self.stack[i].pop() for i in range(3 if self.test else 9))

    def part2(self):
        self.reset()
        for num, fra, til in self.data:
            tempstack = deque()
            for _ in range(num):
                tempstack.append(self.stack[fra - 1].pop())
            for _ in range(num):
                self.stack[til - 1].append(tempstack.pop())
        return "".join(self.stack[i].pop() for i in range(3 if self.test else 9))


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
