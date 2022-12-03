def parseLine(line):
    return line


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        pri = 0
        for l in self.data:
            both = list(set(l[len(l) // 2 :]).intersection(set(l[: len(l) // 2])))[0]
            if both in "abcdefghijklmnopqrstuvwxyz":
                pri += ord(both) - ord("a") + 1
            else:
                pri += ord(both) - ord("A") + 1 + 26
        return pri

    def part2(self):
        pri = 0
        for i in range(0, len(self.data), 3):
            both = list(
                set(self.data[i])
                .intersection(set(self.data[i + 1]))
                .intersection(set(self.data[i + 2]))
            )[0]
            if both in "abcdefghijklmnopqrstuvwxyz":
                pri += ord(both) - ord("a") + 1
            else:
                pri += ord(both) - ord("A") + 1 + 26
        return pri


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
