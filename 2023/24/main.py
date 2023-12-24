import itertools
import random
import re
import time
from sympy import solve, symbols


class Point:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x, self.y, self.z = x, y, z
        self.dx, self.dy, self.dz = dx, dy, dz
        self.a = dy / dx
        self.b = y - self.a * x

    def collision(self, other) -> tuple[float, float]:
        x = (other.b - self.b) / (self.a - other.a)
        y = self.a * x + self.b
        return x, y

    def get_time(self, x):
        return (x - self.x) / self.dx


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            tuple(map(int, re.findall(r"-?\d+", line)))
            for line in open(filename).read().rstrip().split("\n")
        ]

    def get_a_b(self, x, y, z, dx, dy, dz):
        a = dy / dx
        b = y - a * x
        return a, b

    def part1(self):
        points = [Point(*d) for d in self.data]
        start = 200000000000000 if not self.test else 7
        stop = 400000000000000 if not self.test else 27

        ans = 0
        for p1, p2 in itertools.combinations(points, r=2):
            try:
                x, y = p1.collision(p2)
                t1 = p1.get_time(x)
                t2 = p2.get_time(x)
                if t1 < 0 or t2 < 0:
                    continue
                if start <= x <= stop and start <= y <= stop:
                    ans += 1
            except ZeroDivisionError:
                # The pass will never cross, and thats fine
                pass
        return ans

    def part2(self):
        points = random.sample(self.data, 3)

        times = symbols("t1 t2 t3")
        xs = [points[i][0] for i in range(len(points))]
        ys = [points[i][1] for i in range(len(points))]
        zs = [points[i][2] for i in range(len(points))]
        dxs = [points[i][3] for i in range(len(points))]
        dys = [points[i][4] for i in range(len(points))]
        dzs = [points[i][5] for i in range(len(points))]
        p0x, p0y, p0z, dx0, dy0, dz0 = symbols("p0x p0y p0z dx0 dy0 dz0")

        # Create 3 * 3 = 9 equations which should equal 0 (a - b = 0 <=> a = b)
        # ... with 9 unknown: the startposition, velocities and times for collisions
        equations = []
        for i in range(len(points)):
            equations.append(xs[i] + dxs[i] * times[i] - p0x - dx0 * times[i])
            equations.append(ys[i] + dys[i] * times[i] - p0y - dy0 * times[i])
            equations.append(zs[i] + dzs[i] * times[i] - p0z - dz0 * times[i])
        sol = solve(equations)[0]

        return sol[p0x] + sol[p0y] + sol[p0z]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 2 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 47 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
