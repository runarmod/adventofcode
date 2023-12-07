import time
from collections import Counter


def parseLinePart1(line):
    line = (
        line.replace("A", "E")
        .replace("T", "A")
        .replace("J", "B")
        .replace("Q", "C")
        .replace("K", "D")
        .split()
    )
    return list(line[0]), int(line[1])


def parseLinePart2(line):
    line = (
        line.replace("A", "E")
        .replace("T", "A")
        .replace("J", "1")
        .replace("Q", "C")
        .replace("K", "D")
        .split()
    )
    return list(line[0]), int(line[1])


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        content = open(filename).read().rstrip().split("\n")
        self.data1 = map(parseLinePart1, content)
        self.data2 = map(parseLinePart2, content)

    def score(self, cards):
        c = Counter(cards)
        match c.most_common()[0][1]:
            case 5:
                return 6
            case 4:
                return 5
            case 3:
                match c.most_common()[1][1]:
                    case 2:
                        return 4
                    case _:
                        return 3
            case 2:
                match c.most_common()[1][1]:
                    case 2:
                        return 2
                    case _:
                        return 1
            case _:
                return 0

    def best_hand(self, cards):
        if "1" in cards:
            return max(
                [
                    self.best_hand(tuple("".join(cards).replace("1", c, 1)))
                    for c in "23456789ACDE"
                ]
            )
        return self.score(cards)

    def total_rating(self, cards):
        return (self.best_hand(cards), cards)

    def run(self, data):
        l = sorted(data, key=lambda x: self.total_rating(x[0]))
        return sum(bet * i for i, bet in enumerate((x[1] for x in l), start=1))

    def part1(self):
        return self.run(self.data1)

    def part2(self):
        return self.run(self.data2)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    if part1 != 248812215 or part2 != 250057090:
        print("WRONG")
        quit()
    print("CORRECT")


if __name__ == "__main__":
    main()
