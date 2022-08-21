class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split("\t")))
        self.run()

    def run(self):
        self.seen = {}
        self.counter = 0

        while tuple(self.data) not in self.seen:
            self.seen[tuple(self.data)] = self.counter
            idx, val = max(enumerate(self.data), key=lambda x: x[1])
            self.data[idx] = 0

            for i in range(1, val + 1):
                self.data[(idx + i) % len(self.data)] += 1
            self.counter += 1

    def part1(self):
        return self.counter

    def part2(self):
        return self.counter - self.seen[tuple(self.data)]


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
