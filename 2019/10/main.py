import math
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = {
            (x, y)
            for y, line in enumerate(open(filename).read().rstrip().split("\n"))
            for x, c in enumerate(line)
            if c == "#"
        }

    def visible_asteroids(self, coord: tuple[int, int]) -> int:
        sees = len(self.data) - 1
        curr_x, curr_y = coord
        for tmp_x, tmp_y in self.data:
            if (tmp_x, tmp_y) == (curr_x, curr_y):
                continue

            try:
                a = (tmp_y - curr_y) / (tmp_x - curr_x)
            except ZeroDivisionError:
                direction_y = -1 if tmp_y < curr_y else 1
                for y in range(curr_y + direction_y, tmp_y, direction_y):
                    if (curr_x, y) in self.data:
                        sees -= 1
                        break
                continue

            b = tmp_y - a * tmp_x
            direction = -1 if tmp_x < curr_x else 1
            for x in range(curr_x + direction, tmp_x, direction):
                y = a * x + b
                if y - 0.001 < round(y) < y + 0.001:
                    y = round(y)
                    if (x, y) in self.data:
                        sees -= 1
                        break
        return sees

    def part1(self):
        self.optimal_location, visible = max(
            ((coord, self.visible_asteroids(coord)) for coord in self.data),
            key=lambda x: x[1],
        )
        return visible

    def angle(self, coord: tuple[int, int]):
        ang = (
            math.atan2(
                (coord[1] - self.optimal_location[1]),
                coord[0] - self.optimal_location[0],
            )
            + math.pi / 2
        )

        if ang < 0:
            ang += 2 * math.pi
        return ang

    def dist_squared(self, coord: tuple[int, int]):
        return (coord[1] - self.optimal_location[1]) ** 2 + (
            coord[0] - self.optimal_location[0]
        ) ** 2

    def candidates(self, prev_ang: float, ang_lengths: tuple[float, int, int, int]):
        for angle, length, x, y in ang_lengths:
            if angle > prev_ang:
                yield (angle, length, x, y)

    def part2(self):
        points: set[tuple[float, int, int, int]] = set()
        for x, y in self.data:
            if (x, y) == self.optimal_location:
                continue
            points.add((self.angle((x, y)), self.dist_squared((x, y)), x, y))

        prev_ang = -1
        for _ in range(200):
            candidates = list(self.candidates(prev_ang, points))
            if len(candidates) == 0:
                prev_ang = -1
                candidates = list(self.candidates(prev_ang, points))

            removable = min(candidates)
            points.remove(removable)
            prev_ang = removable[0]
        return removable[-2] * 100 + removable[-1]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 210 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 802 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
