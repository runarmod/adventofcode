from collections import defaultdict
import re


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        pattern_rules = re.compile(r"(\w+) => (\w+)")
        self.rules = defaultdict(list)
        with open(filename) as f:
            s = f.read().rstrip()
            for match in pattern_rules.findall(s):
                self.rules[match[0]].append(match[1])
            self.list = s.split("\n")[-1]

        self.list = self.split_upper()

    def split_upper(self):
        tmp = 0
        l = []
        first = True
        for i in range(len(self.list)):
            if self.list[i].isupper() and not first:
                l.append(self.list[tmp:i])
                tmp = i
            first = False
        l.append(self.list[tmp:])
        return l

    def part1(self):
        self.news = set()
        for i, atom in enumerate(self.list):
            for new in self.rules[atom]:
                self.news.add("".join(self.list[:i] + [new] + self.list[i + 1 :]))
        return len(self.news)

    def part2(self):
        return None


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
