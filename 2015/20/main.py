import numpy as np


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.input = int(open(filename).read().rstrip())

    def part1(self):
        return self.answer1

    def part2(self):
        return self.answer2

    def getAnswers(self):
        BIG_NUM = 1000000

        houses_1 = np.zeros(BIG_NUM)
        houses_2 = np.zeros(BIG_NUM)

        for i in range(1, BIG_NUM):
            houses_1[i::i] += 10 * i
            houses_2[i : (i + 1) * 50 : i] += 11 * i
        self.answer1 = np.nonzero(houses_1 >= self.input)[0][0]
        self.answer2 = np.nonzero(houses_2 >= self.input)[0][0]


def main():
    solution = Solution()
    solution.getAnswers()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
