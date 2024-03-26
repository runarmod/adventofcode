import re
import time

from shapely.geometry import Point, Polygon
from shapely.ops import unary_union


def dist(x_1, y_1, x_2, y_2) -> int:
    return abs(x_1 - x_2) + abs(y_1 - y_2)


def parseLine(line):
    s_x, s_y, b_x, b_y = tuple(
        map(
            int,
            re.findall(
                r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
                line,
            )[0],
        )
    )
    return (s_x, s_y), dist(s_x, s_y, b_x, b_y)


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.limit = 10 if self.test else 2000000
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = {
            parseLine(line)[0]: parseLine(line)[1]
            for line in open(filename).read().rstrip().split("\n")
        }

    def part1(self):
        can_not_be = set()
        for (x, y), d in self.data.items():
            extra = max(0, d - abs(self.limit - y))
            for x in range(x - extra, x + extra):
                can_not_be.add(x)
        return len(can_not_be)

    def part2(self):
        polygons = [
            Polygon([(x, y - d), (x + d, y), (x, y + d), (x - d, y), (x, y - d)])
            for (x, y), d in self.data.items()
        ]
        mergedPolys: Polygon = unary_union(polygons)
        hole: Polygon = list(mergedPolys.interiors)[0]
        center: Point = hole.centroid
        return round(center.x) * 4000000 + round(center.y)


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
