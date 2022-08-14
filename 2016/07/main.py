import itertools

# import re
import regex as re


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.input = open(filename).read().rstrip().split("\n")

    def part1(self):
        patternOK = re.compile(r"(?!\[\w*)(\w)(?!\1)(\w)(\2)(\1)(?!\w*\])")
        patternNotOK = re.compile(r"\[\w*(\w)(?!\1)(\w)(\2)(\1)\w*\]")
        return sum(
            1
            for line in self.input
            if patternOK.search(line) and not patternNotOK.search(line)
        )

    def is_ababab(self, sub, hyb):
        return any(
            a == c and a != b and b + a + b in hyb
            for a, b, c in zip(sub, sub[1:], sub[2:])
        )

    def part2(self):
        linesSplitted = [re.split(r"\[|\]", line) for line in self.input]

        supernet = [" ".join(line[::2]) for line in linesSplitted]
        hypernet = [" ".join(line[1::2]) for line in linesSplitted]
        return sum(self.is_ababab(sub, hyb) for sub, hyb in zip(supernet, hypernet))


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
