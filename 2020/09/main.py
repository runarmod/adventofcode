import itertools


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [int(line) for line in open(filename).read().rstrip().split("\n")]

    def find_num(self, size):
        return next(
            (
                self.data[i]
                for i in range(size, len(self.data))
                if all(
                    sum(tup) != self.data[i]
                    for tup in itertools.combinations(self.data[i - size : i], 2)
                )
            ),
            None,
        )

    def part1(self):
        return self.find_num(5 if self.test else 25)

    def part2(self):
        number = self.find_num(5 if self.test else 25)
        for size in range(2, len(self.data)):
            for i in range(len(self.data) - size + 1):
                if sum(self.data[i : i + size]) == number:
                    return min(self.data[i : i + size]) + max(self.data[i : i + size])
        return None


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
