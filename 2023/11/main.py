import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")

        self.expandable_rows = {
            i
            for i in range(len(self.data))
            if all(self.data[i][j] == "." for j in range(len(self.data[i])))
        }
        self.expandable_columns = {
            j
            for j in range(len(self.data[0]))
            if all(self.data[i][j] == "." for i in range(len(self.data)))
        }

    def part1(self):
        return self.calculate()

    def part2(self):
        return self.calculate(((1_000_000 if not self.test else 100) - 1))

    def calculate(self, multiple=1):
        hashtags = (
            (x, y)
            for x in range(len(self.data[0]))
            for y in range(len(self.data))
            if self.data[y][x] == "#"
        )
        s = 0
        for (x1, y1), (x2, y2) in itertools.combinations(hashtags, 2):
            s += multiple * len(
                set(range(min(x1, x2), max(x1, x2))) & self.expandable_columns
            )
            s += multiple * len(
                set(range(min(y1, y2), max(y1, y2))) & self.expandable_rows
            )
            s += abs(x1 - x2) + abs(y1 - y2)
        return s


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


if __name__ == "__main__":
    main()
