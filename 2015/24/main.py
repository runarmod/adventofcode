from functools import reduce
from itertools import chain, combinations
from operator import mul


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.weights = tuple(map(int, open(filename).read().rstrip().split("\n")))

    def run(self, v):
        self.individualWeight = sum(self.weights) // v
        for i in range(len(self.weights)):
            if qes := [
                reduce(mul, c)
                for c in combinations(self.weights, i)
                if sum(c) == self.individualWeight
            ]:
                return min(qes)

    def part1(self):
        return self.run(3)

    def part2(self):
        return self.run(4)


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
