def parseLine(line):
    return int(line)


class Solution:
    def __init__(self, test=False):
        self.test = test

    def reset(self):
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]
        self.i = 0
        self.steps = 0

    def jump(self, part):
        offset = -1 if part == 2 and self.data[self.i] >= 3 else 1
        self.data[self.i], self.i = (
            self.data[self.i] + offset,
            self.i + self.data[self.i],
        )

        self.steps += 1
        return self.i < len(self.data)

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)

    def run(self, part):
        self.reset()
        while self.jump(part):
            pass
        return self.steps


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
