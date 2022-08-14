import re
import numpy as np


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.inn = open(filename).read()

    def part1(self):
        return sum(
            int(match[0]) * int(match[1])
            for match in re.compile(r"(\d+)x(\d+)").findall(self.inn)
        )

    def display(self, s):
        print("\n".join("".join("#" if c else " " for c in row) for row in s))

    def part2(self):
        pattern = re.compile(
            r"(?:(rect) (\d+)x(\d+))|(?:(rotate) (column|row) (x|y)=(\d+)) by (\d+)"
        )
        screen = np.zeros((6, 50), dtype=int)
        for match in pattern.finditer(self.inn):
            rect = match[1] == "rect"
            if rect:
                x, y = int(match[2]), int(match[3])
                screen[:y, :x] = 1
            else:
                column = match[5] == "column"
                if column:
                    x_axis, amount = int(match[7]), int(match[8])
                    screen[:, x_axis] = np.roll(screen[:, x_axis], amount)
                else:
                    y_axis, amount = int(match[7]), int(match[8])
                    screen[y_axis] = np.roll(screen[y_axis], amount)
        self.display(screen)
        return "ZJHRKCPLYJ"


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
