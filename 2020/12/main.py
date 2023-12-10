import re
import time


class Ship1:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction

    def rotate_left(self):
        self.dir *= 1j

    def rotate_right(self):
        self.dir /= 1j

    def move(self, direction: str, length: int):
        match direction:
            case "N":
                self.y += length
            case "S":
                self.y -= length
            case "E":
                self.x += length
            case "W":
                self.x -= length
            case "L":
                for _ in range(length // 90):
                    self.rotate_left()
            case "R":
                for _ in range(length // 90):
                    self.rotate_right()
            case "F":
                self.x += length * self.dir.real
                self.y += length * self.dir.imag
            case _:
                raise ValueError(f"Invalid direction: {direction}")


class Ship2:
    def __init__(self, waypoint_east, waypoint_north, ship_east, ship_north):
        self.waypoint_east = waypoint_east
        self.waypoint_north = waypoint_north
        self.ship_east = ship_east
        self.ship_north = ship_north

    def rotate_left(self):
        coord = self.waypoint_east + self.waypoint_north * 1j
        coord *= 1j
        self.waypoint_east = coord.real
        self.waypoint_north = coord.imag

    def rotate_right(self):
        coord = self.waypoint_east + self.waypoint_north * 1j
        coord /= 1j
        self.waypoint_east = coord.real
        self.waypoint_north = coord.imag

    def move(self, direction: str, length: int):
        match direction:
            case "N":
                self.waypoint_north += length
            case "S":
                self.waypoint_north -= length
            case "E":
                self.waypoint_east += length
            case "W":
                self.waypoint_east -= length
            case "L":
                for _ in range(length // 90):
                    self.rotate_left()
            case "R":
                for _ in range(length // 90):
                    self.rotate_right()
            case "F":
                self.ship_east += length * self.waypoint_east
                self.ship_north += length * self.waypoint_north
            case _:
                raise ValueError(f"Invalid direction: {direction}")


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            (line[0], list(map(int, re.findall(r"\d+", line)))[0])
            for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        c = Ship1(0, 0, 1 + 0j)
        for d, length in self.data:
            c.move(d, length)
        return int(abs(c.x) + abs(c.y))

    def part2(self):
        c = Ship2(10, 1, 0, 0)
        for d, length in self.data:
            c.move(d, length)
        return int(abs(c.ship_east) + abs(c.ship_north))


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
