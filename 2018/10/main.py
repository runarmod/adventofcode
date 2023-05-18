import re
import time


def parseLine(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.marbles = tuple(map(parseLine, open(filename).read().rstrip().split("\n")))
        self.run()

    def area(self, marbles):
        max_x = max_y = -float("inf")
        min_x = min_y = float("inf")
        for marble in marbles:
            max_x = max(max_x, marble[0])
            max_y = max(max_y, marble[1])
            min_x = min(min_x, marble[0])
            min_y = min(min_y, marble[1])
        return (max_x - min_x) * (max_y - min_y)

    def show(self, lst):
        coords = lst

        max_x, min_x = max(marble[0] for marble in coords), min(marble[0] for marble in coords)
        max_y, min_y = max(marble[1] for marble in coords), min(marble[1] for marble in coords)
        new_coords = {(x, -y) for x, y in coords}
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, -y) in new_coords:
                    print("█", end="")
                else:
                    print(" ", end="")
            print()

    def get_area_marbles(self, time):
        marbles = tuple(
            (marble[0] + marble[2] * time, marble[1] + marble[3] * time) for marble in self.marbles
        )
        area = self.area(marbles)
        return area, marbles

    def find_lowest_area(self, low, high):
        if high < low:
            return self.get_area_marbles(0)[1], 0

        if high == low:
            return self.get_area_marbles(low)[1], low

        mid = (low + high) // 2

        # Mid is lowest point
        if (
            self.get_area_marbles(mid - 1)[0]
            > self.get_area_marbles(mid)[0]
            < self.get_area_marbles(mid + 1)[0]
        ):
            return self.get_area_marbles(mid)[1], mid

        # Gets lower to the right
        if self.get_area_marbles(mid - 1)[0] > self.get_area_marbles(mid)[0]:
            return self.find_lowest_area(mid + 1, high)

        # Gets lower to the left
        if self.get_area_marbles(mid)[0] < self.get_area_marbles(mid + 1)[0]:
            return self.find_lowest_area(low, mid - 1)

    def run(self):
        self.winning_coords, self.result2 = self.find_lowest_area(0, 20_000)

    def part1(self):
        self.show(self.winning_coords)
        self.result1 = "HI" if self.test else "FNRGPBHR"
        return self.result1

    def part2(self):
        return self.result2


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
