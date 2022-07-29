from calendar import c


class Solution():
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")

    def literalToMemorySize(self, s):
        size = len(s) - 2

        i = 1
        while i < len(s) - 2:
            if s[i:i+2] == "\\\\":
                size -= 1
                i += 2
                continue
            if s[i:i+2] == "\\\"":
                size -= 1
                i += 2
                continue
            if s[i:i+2] == "\\x":
                size -= 3
                i += 4
                continue
            i += 1
        return size

    def memoryToLiteralSize(self, s):
        return len(s) + sum(c in ["\\", "\""] for c in s) + 2

    def part1(self):
        return sum(len(d) for d in self.data) - sum(self.literalToMemorySize(d) for d in self.data)

    def part2(self):
        return sum(self.memoryToLiteralSize(d) for d in self.data) - sum(len(d) for d in self.data)


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
