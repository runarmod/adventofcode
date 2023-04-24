import re


def parseLine(line):
    pattern = re.compile(r"(\d+)? ?(\w+ \w+) bags?")
    _all = re.findall(pattern, line)
    bags = [(int(_all[i][0]), _all[i][1]) for i in range(1, len(_all)) if _all[i][1] != "no other"]

    return [(_all[0][1], bags)]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = {
            key: val
            for line in open(filename).read().rstrip().split("\n")
            for key, val in parseLine(line)
        }

    def hasBag(self, bag, target):
        return bag == target or any(self.hasBag(b, target) for _, b in self.data[bag])

    def part1(self):
        return sum(self.hasBag(bag, "shiny gold") for bag in self.data if bag != "shiny gold")

    def countBags(self, bag):
        return 1 + sum(count * self.countBags(b) for count, b in self.data[bag])

    def part2(self):
        return self.countBags("shiny gold") - 1


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
