import re
from collections import defaultdict


def parseLine(line):
    var, op, amount, dependant, comparator, value = re.findall(
        r"(\w+) (inc|dec) (-?\d+) if (\w+) ([<=>!]+) (-?\d+)", line
    )[0]
    amount, value = int(amount), int(value)
    op = (lambda x: x + amount) if op == "inc" else (lambda x: x - amount)
    condition = (
        lambda x: x >= value
        if comparator == ">="
        else x <= value
        if comparator == "<="
        else x > value
        if comparator == ">"
        else x < value
        if comparator == "<"
        else x == value
        if comparator == "=="
        else x != value
    )

    return var, op, dependant, condition


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]
        self.variables = defaultdict(lambda: 0)
        self.answers = {1: 0, 2: 0}
        self.run()

    def run(self):
        for variable, operation, dependant, condition in self.data:
            if condition(self.variables[dependant]):
                self.variables[variable] = operation(self.variables[variable])
                self.answers[2] = max(
                    self.answers[2],
                    self.variables[max(self.variables, key=lambda x: self.variables[x])],
                )
        self.answers[1] = self.variables[max(self.variables, key=lambda x: self.variables[x])]

    def part1(self):
        return self.answers[1]

    def part2(self):
        return self.answers[2]


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
