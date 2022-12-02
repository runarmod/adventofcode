from collections import defaultdict


def parseLine(line):
    they, me = line.split(" ")
    they, me = ord(they) - ord("A") + 1, ord(me) - ord("X") + 1
    return they, me


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def calculate_score(self, hand1, hand2):
        score = hand2
        if hand1 == hand2:
            score += 3
        else:
            hand2 = 4 if hand2 == 1 else hand2
            if hand1 + 1 == hand2:
                score += 6
        return score

    def part1(self):
        score = 0
        for line in self.data:
            score += self.calculate_score(line[0], line[1])
        return score

    def part2(self):
        score = 0
        for line in self.data:
            move = None
            if line[1] == 2:
                move = line[0]
            elif line[1] == 3:
                move = line[0] + 1 if line[0] < 3 else 1
            elif line[1] == 1:
                move = line[0] - 1 if line[0] > 1 else 3
            score += self.calculate_score(line[0], move)
        return score


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
