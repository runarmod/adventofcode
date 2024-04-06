import string


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(open(filename).read().rstrip().split("\n"))

    def calculate_score(self, c):
        if c in string.ascii_lowercase:
            return ord(c) - ord("a") + 1
        return ord(c) - ord("A") + 1 + 26

    def part1(self):
        pri = 0
        for l in self.data:
            both = list(set(l[len(l) // 2 :]).intersection(set(l[: len(l) // 2])))[0]
            pri += self.calculate_score(both)
        return pri

    def separate_to_3(self, data):
        for i in range(0, len(data), 3):
            yield map(set, data[i : i + 3])

    def part2(self):
        pri = 0
        for first, second, third in self.separate_to_3(self.data):
            both = list(first.intersection(second).intersection(third))[0]
            pri += self.calculate_score(both)
        return pri


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
