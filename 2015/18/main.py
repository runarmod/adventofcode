import itertools
import numpy as np


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.steps = 4 if self.test else 100
        self.original = (
            open("testinput.txt" if self.test else "input.txt")
            .read()
            .rstrip()
            .split("\n")
        )

        self.original = np.array(
            [[c == "#" for c in line] for line in self.original]
        ).astype(int)
        self.original = np.pad(self.original, 1, "constant", constant_values=0)

    def step(self, part2=False):
        for i in range(1, len(self.data) - 1):
            for j in range(1, len(self.data[i]) - 1):
                if self.data[i][j]:
                    if self.count_bugs(i, j) not in (2, 3):
                        self.temp[i][j] = not self.data[i][j]
                elif self.count_bugs(i, j) == 3:
                    self.temp[i][j] = not self.data[i][j]
        self.data = self.temp.copy()
        if part2:
            self.keepCornersOn()

    def keepCornersOn(self):
        self.data[1][1] = 1
        self.data[1][len(self.data[1]) - 2] = 1
        self.data[len(self.data) - 2][1] = 1
        self.data[len(self.data) - 2][len(self.data[1]) - 2] = 1

    def count_bugs(self, i, j):
        return sum(
            self.data[i + y][j + x]
            for y, x in itertools.product(range(-1, 2), range(-1, 2))
            if y != 0 or x != 0
        )

    def part1(self):
        self.data = self.original.copy()
        self.temp = self.data.copy()

        for _ in range(self.steps):
            self.step()
        return self.data.sum()

    def part2(self):
        self.data = self.original.copy()
        self.temp = self.data.copy()

        self.keepCornersOn()
        for _ in range(self.steps):
            self.step(part2=True)
        return self.data.sum()


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
