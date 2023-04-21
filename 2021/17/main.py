import itertools
import re


def parseLine(line):
    return list(
        map(int, re.findall(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", line)[0])
    )


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.x_left, self.x_right, self.y_bottom, self.y_top = parseLine(
            open(filename).read().rstrip()
        )

    def find_x(self):
        for i in range(1, self.x_right + 1):
            x_coords = tuple(
                itertools.accumulate(
                    map(lambda x: x, range(i, 0, -1)), lambda x, y: x + y, initial=0
                )
            )
            if any(self.x_left <= x <= self.x_right for x in x_coords):
                yield i

    def works(self, x_speed, y_speed):
        x = y = 0
        while x <= self.x_right and y >= self.y_bottom:
            if self.x_left <= x <= self.x_right and self.y_bottom <= y <= self.y_top:
                return True
            x += x_speed
            y += y_speed
            x_speed = x_speed - 1 if x_speed > 0 else (x_speed + 1 if x_speed < 0 else 0)
            y_speed -= 1
        return False

    def tallest(self, x_speed, y_speed):
        x = y = 0
        while x <= self.x_right and y >= self.y_bottom:
            if self.x_left <= x <= self.x_right and self.y_bottom <= y <= self.y_top:
                return None
            if y_speed == 0:
                return y
            x += x_speed
            y += y_speed
            x_speed = x_speed - 1 if x_speed > 0 else (x_speed + 1 if x_speed < 0 else 0)
            y_speed -= 1
        return None

    def part1(self):
        x_speeds = tuple(self.find_x())
        for y_speed_start in range(200, 0, -1):
            for x_speed_start in x_speeds:
                if self.works(x_speed_start, y_speed_start):
                    return self.tallest(x_speed_start, y_speed_start)
        return None

    def part2(self):
        x_speeds = tuple(self.find_x())
        count = 0
        for y_speed_start in range(200, -200, -1):
            for x_speed_start in x_speeds:
                if self.works(x_speed_start, y_speed_start):
                    count += 1
        return count


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
