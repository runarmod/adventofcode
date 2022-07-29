import re
import os
import timeit


infile = os.path.join(os.path.dirname(__file__), "../input.txt")


class LightArray(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = [[False for _ in range(height)] for _ in range(width)]

    def display(self):
        """ Return ascii-art image of the array. """
        lines = []
        for row in range(self.height):
            y = self.height - row - 1
            line = ["."] * self.width
            for x in range(self.width):
                if self.array[x][y]:
                    line[x] = "@"
            lines.append("".join(line))
        return "\n".join(lines)

    def count_on(self):
        return sum(column.count(True) for column in self.array)

    def set_region(self, start, end, value):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] = value

    def toggle_region(self, start, end):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] = not self.array[x][y]


line_re = re.compile(
    r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")


def findCommandAndCoords(line):
    match = line_re.match(line).groups() # command, x0, y0, x1, y1
    return match[0], *(int(match[i]) for i in range(1,5))


def part1():
    with open(infile, "r") as fp:
        inn = fp.read()
    print("Part 1")
    lights = LightArray(1000, 1000)

    for line in inn.splitlines():
        op, x0, y0, x1, y1 = findCommandAndCoords(line)
    
        if op == "turn on":
            lights.set_region((x0, y0), (x1, y1), True)
        elif op == "turn off":
            lights.set_region((x0, y0), (x1, y1), False)
        elif op == "toggle":
            lights.toggle_region((x0, y0), (x1, y1))

    print(lights.count_on(), "lights lit")

    with open("output.txt", "w") as f:
        for line in lights.array:
            for c in line:
                f.write("@" if c else " ")
            f.write("\n")


commands = ["toggle", "turn on", "turn off"]

if __name__ == '__main__':

    print(f"{timeit.timeit(part1, number=1):.2f}")
    
