import itertools


class Solution():
    def __init__(self, test=False):
        self.test = test
        self.eggnog = 25 if self.test else 150
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = sorted(
            list(map(int, open(filename).read().rstrip().split("\n"))))

        self.run()

    def run(self):
        self._part1 = 0
        self._used = []
        for i in range(1, len(self.data)):
            for t in itertools.combinations(self.data, i):
                if sum(t) == self.eggnog:
                    self._part1 += 1
                    self._used.append(t)

    def part1(self):
        return self._part1

    def part2(self):
        # number of occurrences where the length of the list is the same as the length of the shortest list where the sum is equal to the target
        return sum(len(l) == len(min(self._used, key=len)) for l in self._used)


def main():
    solution = Solution(test=0)
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
