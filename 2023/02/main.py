import time
from collections import defaultdict


def parseLine(line):
    line_data = []
    splitted = line.split(" ")
    line_data.append(int(splitted[1][:-1]))
    subsection = []
    for i in range(2, len(splitted), 2):
        if splitted[i + 1][-1] == ";":
            subsection.append((int(splitted[i]), splitted[i + 1][:-1]))
            line_data.append(subsection)
            subsection = []
        elif splitted[i + 1][-1] == ",":
            subsection.append((int(splitted[i]), splitted[i + 1][:-1]))
        else:
            subsection.append((int(splitted[i]), splitted[i + 1]))
    if subsection:
        line_data.append(subsection)
    return line_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        return sum(line[0] for line in self.data if self.possible(line))

    def possible(self, line):
        for instance in line[1:]:
            green = sum(a[0] for a in instance if a[1] == "green")
            red = sum(a[0] for a in instance if a[1] == "red")
            blue = sum(a[0] for a in instance if a[1] == "blue")
            if red > 12 or green > 13 or blue > 14:
                return False
        return True

    def part2(self):
        sum_power_of_sets = 0
        for line in self.data:
            game = defaultdict(int)
            for instance in line[1:]:
                for color in ("green", "red", "blue"):
                    game[color] = max(
                        game[color], sum(a[0] for a in instance if a[1] == color)
                    )
            sum_power_of_sets += game["green"] * game["red"] * game["blue"]
        return sum_power_of_sets


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
