class Solution():
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")

    def part1(self):
        return None

    def part2(self):
        return None


def main():
    solution = Solution(test=True)
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
