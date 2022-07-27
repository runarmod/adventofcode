import re
import os
import timeit


infile = os.path.join(os.path.dirname(__file__), "../input.txt")


class LightArray(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = [[0 for _ in range(height)] for _ in range(width)]

    # def display(self):
    #     """ Return ascii-art image of the array. """
    #     lines = []
    #     for row in range(self.height):
    #         y = self.height - row - 1
    #         line = ["."] * self.width
    #         for x in range(self.width):
    #             if self.array[x][y]:
    #                 line[x] = "@"
    #         lines.append("".join(line))
    #     return "\n".join(lines)

    def total_brightness(self):
        return sum(map(sum, self.array))

    def turn_on(self, coords):
        for y in range(coords[1], coords[3]+1):
            for x in range(coords[0], coords[2]+1):
                self.array[y][x] += 1

    def turn_off(self, coords):
        for y in range(coords[1], coords[3]+1):
            for x in range(coords[0], coords[2]+1):
                self.array[y][x] = max(self.array[y][x] - 1, 0)

    def toggle_region(self, coords):
        for y in range(coords[1], coords[3]+1):
            for x in range(coords[0], coords[2]+1):
                self.array[y][x] += 2


def findCommandAndCoords(line):
    line_re = re.compile(
        r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")
    match = line_re.match(line).groups()  # command, x0, y0, x1, y1
    return match[0], [int(match[i]) for i in range(1, 5)]


def part2():
    with open(infile, "r") as fp:
        inn = fp.read()
    print("Part 2")
    lights = LightArray(1000, 1000)

    for line in inn.splitlines():
        op, coords = findCommandAndCoords(line)

        if op == "turn on":
            lights.turn_on(coords)
        elif op == "turn off":
            lights.turn_off(coords)
        elif op == "toggle":
            lights.toggle_region(coords)

    print(lights.total_brightness(), "total brightness")


if __name__ == '__main__':
    print(f"{timeit.timeit(part2, number=1):.2f}")
