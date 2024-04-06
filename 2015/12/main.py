import re
from json import loads


class Solution():
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()
        self.jsn = loads(self.data)

    def n(self, j):
        if type(j) == int:
            return j
        if type(j) == list:
            return sum(self.n(i) for i in j)
        if type(j) != dict:
            return 0
        if "red" in j.values():
            return 0
        return self.n(list(j.values()))

    def part1(self):
        return sum(map(int, re.findall(r"(-?\d+)", self.data)))

    def part2(self):
        return self.n(self.jsn)


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
