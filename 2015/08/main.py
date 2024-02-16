class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")

    def memoryToLiteralSize(self, s):
        return len(s) + sum(c in ["\\", '"'] for c in s) + 2

    def part1(self):
        return sum(len(d) for d in self.data) - sum(len(eval(d)) for d in self.data)

    def part2(self):
        return sum(self.memoryToLiteralSize(d) for d in self.data) - sum(
            len(d) for d in self.data
        )


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
