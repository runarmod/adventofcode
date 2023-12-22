import itertools
import time
from collections import defaultdict, deque


def parseLine(line):
    first_corner, second_corner = line.split("~")
    first_corner = list(map(int, first_corner.split(",")))
    second_corner = list(map(int, second_corner.split(",")))
    return (
        range(
            min(first_corner[0], second_corner[0]),
            max(first_corner[0], second_corner[0]) + 1,
        ),
        range(
            min(first_corner[1], second_corner[1]),
            max(first_corner[1], second_corner[1]) + 1,
        ),
        range(
            min(first_corner[2], second_corner[2]),
            max(first_corner[2], second_corner[2]) + 1,
        ),
    )


class Cube:
    def __init__(self, x_r, y_r, z_r):
        self.x_r = x_r
        self.y_r = y_r
        self.z_r = z_r
        self.height = self.z_r.stop - self.z_r.start

    def fall(self, setled):
        for z in range(self.z_r.start - 1, 0, -1):
            for x in self.x_r:
                for y in self.y_r:
                    if (x, y, z) in setled:
                        self.z_r = range(z + 1, self.height + z)
                        return {
                            (nx, ny, self.z_r.stop)
                            for nx, ny in itertools.product(self.x_r, self.y_r)
                        }
        self.z_r = range(1, self.height)
        return {
            (nx, ny, self.z_r.stop) for nx, ny in itertools.product(self.x_r, self.y_r)
        }


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            Cube(*parseLine(line))
            for line in open(filename).read().rstrip().split("\n")
        ]

        self.data.sort(key=lambda cube: cube.z_r.start)
        self.generate_above_below()

    def generate_above_below(self):
        setled_tops = {}
        for cube in self.data:
            for coord in cube.fall(setled_tops):
                setled_tops[coord] = cube

        self.cubes_below = defaultdict(set)
        self.cubes_above = defaultdict(set)

        for cube in self.data:
            for x in cube.x_r:
                for y in cube.y_r:
                    if (x, y, cube.z_r.start - 1) in setled_tops:
                        self.cubes_below[cube].add(
                            setled_tops[(x, y, cube.z_r.start - 1)]
                        )
                        self.cubes_above[setled_tops[(x, y, cube.z_r.start - 1)]].add(
                            cube
                        )

    def part1(self):
        return sum(
            1
            for cube in self.data
            if len(self.cubes_above[cube]) == 0
            or all(len(self.cubes_below[cube2]) > 1 for cube2 in self.cubes_above[cube])
        )

    def part2(self):
        s = 0
        for start_cube in self.data:
            q = deque()
            q.append(start_cube)
            cubes_falling = set()
            while q:
                current_cube = q.popleft()
                if current_cube in cubes_falling:
                    continue
                cubes_falling.add(current_cube)
                s += 1
                for nxt in self.cubes_above[current_cube]:
                    if not self.cubes_below[nxt] - cubes_falling:
                        q.append(nxt)
            s -= 1
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1},\t{'correct :)' if test1 == 5 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2},\t{'correct :)' if test2 == 7 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
