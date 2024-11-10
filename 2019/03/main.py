import re


def parseLine(line):
    return re.findall(r"(R|L|D|U)(\d+)", line)


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]
        self.line1 = self.generate_points(self.data[0])
        self.line2 = self.generate_points(self.data[1])
        self.crosses = self.line1.keys() & self.line2.keys()

    def generate_points(self, line):
        visited = {}
        time = 0
        x, y = 0, 0
        for direction, length in line:
            for _ in range(int(length)):
                time += 1
                if direction == "D":
                    y -= 1
                elif direction == "L":
                    x -= 1
                elif direction == "R":
                    x += 1
                elif direction == "U":
                    y += 1
                if (x, y) not in visited:
                    visited[(x, y)] = time
        return visited

    def part1(self):
        return min(abs(x) + abs(y) for x, y in self.crosses)

    def part2(self):
        return min(self.line1[cross] + self.line2[cross] for cross in self.crosses)


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
