import re


def parseLine(line):
    return tuple(
        match
        for match in re.match(r"(s)(\d+)|(x)(\d+)\/(\d+)|(p)(\w+)\/(\w+)", line).groups()
        if match is not None
    )


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(parseLine, open(filename).read().rstrip().split(",")))

        self.lst = [chr(c) for c in range(ord("a"), (ord("e") if self.test else ord("p")) + 1)]
        self.seen = []

    def round(self):
        if self.get_string() in self.seen:
            return self.seen[1_000_000_000 % len(self.seen)]
        self.seen.append(self.get_string())

        for group in self.data:
            match group[0]:
                case "s":
                    length = int(group[1])
                    self.lst = self.lst[-length:] + self.lst[:-length]
                case "x":
                    first, second = int(group[1]), int(group[2])
                    self.lst[first], self.lst[second] = self.lst[second], self.lst[first]
                case "p":
                    first, second = self.lst.index(group[1]), self.lst.index(group[2])
                    self.lst[first], self.lst[second] = self.lst[second], self.lst[first]
        return None

    def get_string(self):
        return "".join(self.lst)

    def part1(self):
        self.round()
        return self.get_string()

    def part2(self):
        for _ in range(1, 1_000_000_000):
            if (ans := self.round()) is not None:
                return ans
        return "No answer"


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
