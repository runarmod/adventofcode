class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split("\n")))

    def calculate_fuel(self, mass, part):
        fuel = mass // 3 - 2
        return (
            0
            if fuel <= 0
            else fuel + (0 if part == 1 else self.calculate_fuel(fuel, part))
        )

    def calculate(self, part):
        return sum(self.calculate_fuel(i, part) for i in self.data)

    def part1(self):
        return self.calculate(1)

    def part2(self):
        return self.calculate(2)


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
