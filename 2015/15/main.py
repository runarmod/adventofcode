import re
from math import prod


class Solution():
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()
        self.pattern = re.compile(
            r"(\w+): capacity (.?\d+), durability (.?\d+), flavor (.?\d+), texture (.?\d+), calories (.?\d+)")
        self.ingredients = [(ing, int(cap), int(dur), int(flav), int(tex), int(
            cal)) for ing, cap, dur, flav, tex, cal in self.pattern.findall(self.data)]

    def run(self, part):
        record = 0
        for x1 in range(101):
            for x2 in range(101 - x1):
                for x3 in range(101 - x1 - x2):
                    x4 = 100 - x3 - x2 - x1
                    l = [max(0, self.ingredients[0][i] * x1 + self.ingredients[1][i] * x2 +
                             self.ingredients[2][i] * x3 + self.ingredients[3][i] * x4) for i in range(1, 5)]
                    if part == 1 or self.ingredients[0][5] * x1 + self.ingredients[1][5] * x2 + self.ingredients[2][5] * x3 + self.ingredients[3][5] * x4 == 500:
                        record = max(record, prod(l))
        return record

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)


def main():
    # Not implemented test
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
