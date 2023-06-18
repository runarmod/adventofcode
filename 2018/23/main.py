import itertools
import re
import time
from collections import namedtuple


def parseLine(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]
        self.in_range_count = {}

    def distance(self, coord1: tuple[int, int, int, int], coord2: tuple[int, int, int, int]):
        return sum(abs(c1 - c2) for c1, c2 in zip(coord1[:3], coord2[:3]))

    def part1(self):
        p1 = max(self.data, key=lambda p: p[3])
        return self.in_range_point_range(p1)

    def in_range_point_range(self, p):
        return sum(self.distance(p, p2) <= p[3] for p2 in self.data)

    def in_range_point(self, p: tuple[int, int, int]):
        if p not in self.in_range_count:
            self.in_range_count[p] = sum(self.distance(p, p2) <= p2[3] for p2 in self.data)
        return self.in_range_count[p]

    def part2(self):
        min_x, max_x = min(p[0] for p in self.data), max(p[0] for p in self.data)
        min_y, max_y = min(p[1] for p in self.data), max(p[1] for p in self.data)
        min_z, max_z = min(p[2] for p in self.data), max(p[2] for p in self.data)
        point = namedtuple("Point", "x y z count")

        while (max_x - min_x) * (max_y - min_y) * (max_z - min_z) > 10:
            best = point(0, 0, 0, 0)
            x_step = max(1, (max_x - min_x) // 3)
            y_step = max(1, (max_y - min_y) // 3)
            z_step = max(1, (max_z - min_z) // 3)
            for x, y, z in itertools.product(
                range(min_x, max_x + 1, x_step),
                range(min_y, max_y + 1, y_step),
                range(min_z, max_z + 1, z_step),
            ):
                p = (x, y, z)
                c = self.in_range_point(p)
                if c > best.count:
                    best = point(x, y, z, c)
            min_x, max_x = best.x - x_step, best.x + x_step
            min_y, max_y = best.y - y_step, best.y + y_step
            min_z, max_z = best.z - z_step, best.z + z_step

        point = namedtuple("Point", "x y z distance")
        best = point(0, 0, 0, 0)
        for x, y, z in itertools.product(
            range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1)
        ):
            p = (x, y, z)
            c = self.in_range_point(p)
            if c > best.distance:
                best = point(*p, c)
        return self.distance((0, 0, 0, 0), (best.x, best.y, best.z, 0))


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
