from collections import defaultdict
import itertools
import re
import string
from pprint import pprint


def parseLine(line):
    return re.findall(r"(?:(\$) )?(cd|ls)?(dir|\d+)? ([\w\./]+)?", line)[0]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]
        self.summ = 0

    def navigate(self, pos, line, dir):
        i = self.system
        for s in pos:
            i = i[s]

        if dir:
            i[line[3]] = defaultdict(set)
        else:
            i[line[3]] = int(line[2])

    def set_size_and_find_part1_answer(self, system):
        s = 0
        for k, v in system.items():
            if type(v) == int:
                s += v
            else:
                s += self.set_size_and_find_part1_answer(v)

        if s < 100000:
            self.summ += s
        system["size"] = s
        return s

    def part1(self):
        pos = ["/"]
        self.system = {
            "/": defaultdict(set),
        }
        for line in self.data:
            if line[0] == "$" and line[1] == "cd":
                if line[3] == "/":
                    pos = ["/"]
                elif line[3] == "..":
                    pos.pop()
                else:
                    pos.append(line[3])
            elif line[2] == "dir":
                self.navigate(pos, line, True)
            elif line[2].isdigit():
                self.navigate(pos, line, False)

        self.set_size_and_find_part1_answer(self.system)
        return self.summ

    def part2(self):
        has_to_free = self.system["size"] - 40000000
        going_to_free = float("inf")

        def help(system):
            nonlocal going_to_free
            for k, v in system.items():
                if type(v) != int:
                    if "size" in v and v["size"] >= has_to_free:
                        going_to_free = min(going_to_free, v["size"])
                    help(v)

        help(self.system)
        return going_to_free


def main():
    test = Solution(test=True)
    print(part1_test := f"(TEST) Part 1: {test.part1()}")
    print(part2_test := f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
