import re
import sys
import time

sys.setrecursionlimit(10_000)


def parseData(lines):
    blocks = set()
    for line in lines:
        coords = list(map(int, re.findall(r"\d+", line)))
        if line[0] == "x":
            for y in range(coords[1], coords[2] + 1):
                blocks.add((coords[0], y))
        else:
            for x in range(coords[1], coords[2] + 1):
                blocks.add((x, coords[0]))
    return blocks


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.clay = parseData(open(filename).read().rstrip().split("\n"))

        self.settled = set()
        self.flowing = set()

        self.min_x = min(x for x, y in self.clay)
        self.max_x = max(x for x, y in self.clay)
        self.min_y = min(y for x, y in self.clay)
        self.max_y = max(y for x, y in self.clay)

        self.place_water((500, 0))
        # self.write_map()

    def write_map(self):
        min_x = min(x for x, y in self.flowing.union(set(self.clay)))
        max_x = max(x for x, y in self.flowing.union(set(self.clay)))
        min_y = min(y for x, y in self.flowing.union(set(self.clay)))
        max_y = max(y for x, y in self.flowing.union(set(self.clay)))
        with open("map.txt", "w") as f:
            for y in range(min_y, max_y + 2):
                for x in range(min_x - 1, max_x + 2):
                    f.write(
                        "#"
                        if (x, y) in self.clay
                        else "~"
                        if (x, y) in self.settled
                        else "|"
                        if (x, y) in self.flowing
                        else "."
                    )
                f.write("\n")

    def place_water(self, pt, direction=(0, 1)):
        self.flowing.add(pt)

        under = (pt[0], pt[1] + 1)

        if under not in self.clay and under not in self.flowing and 1 <= under[1] <= self.max_y:
            self.place_water(under)

        if under not in self.clay and under not in self.settled:
            return False

        left = (pt[0] - 1, pt[1])
        right = (pt[0] + 1, pt[1])

        left_filled = (
            left in self.clay
            or left not in self.flowing
            and self.place_water(left, direction=(-1, 0))
        )

        right_filled = (
            right in self.clay
            or right not in self.flowing
            and self.place_water(right, direction=(1, 0))
        )

        if direction == (0, 1) and left_filled and right_filled:
            self.settled.add(pt)

            while left in self.flowing:
                self.settled.add(left)
                left = (left[0] - 1, left[1])

            while right in self.flowing:
                self.settled.add(right)
                right = (right[0] + 1, right[1])

        return (
            direction == (-1, 0)
            and (left_filled or left in self.clay)
            or direction == (1, 0)
            and (right_filled or right in self.clay)
        )

    def part1(self):
        return len([c for c in self.flowing | self.settled if self.min_y <= c[1] <= self.max_y])

    def part2(self):
        return len([c for c in self.settled if self.min_y <= c[1] <= self.max_y])


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
