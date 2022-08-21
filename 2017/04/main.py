class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.lines = [
            line.split(" ") for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        return sum(len(set(line)) == len(line) for line in self.lines)

    def part2(self):
        return sum(
            len({"".join(sorted(word)) for word in line}) == len(line)
            for line in self.lines
        )


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
