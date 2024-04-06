import re


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.compressed = open(filename).read().strip()

    def decode(self, line, part2=False):
        if not line or line[0] != "(":
            return 1 + self.decode(line[1:], part2) if line else 0
        match = re.match(r"\((\d+)x(\d+)\)", line)
        length, repeat = map(int, match.groups())
        return repeat * (
            self.decode(line[match.end() : match.end() + length], part2)
            if part2
            else len(line[match.end() : match.end() + length])
        ) + self.decode(line[match.end() + length :], part2)

    def part1(self):
        return self.decode(self.compressed)

    def part2(self):
        return self.decode(self.compressed, part2=True)


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
