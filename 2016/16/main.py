class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.start = open(filename).read().rstrip()
        self.length1 = 20 if self.test else 272
        self.length2 = 20 if self.test else 35651584

    def iteration(self, a):
        b = "".join("1" if c == "0" else "0" for c in reversed(a))
        return f"{a}0{b}"

    def checksum(self, string):
        checksum = string
        while len(checksum) % 2 == 0:
            checksum = "".join(str(int(a == b)) for a, b in zip(checksum[::2], checksum[1::2]))
        return checksum

    def run(self, length):
        string = self.start
        while len(string) < length:
            string = self.iteration(string)
        return self.checksum(string[:length])

    def part1(self):
        return self.run(self.length1)

    def part2(self):
        return self.run(self.length2)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
