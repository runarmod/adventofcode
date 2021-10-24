import re

infile = "../input.txt"

class LightArray(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = [[False for row in range(height)] for col in range(width)]

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
        count = 0
        for column in self.array:
            count += column.count(True)
        return count

    def set_region(self, start, end, value):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] = value

    def toggle_region(self, start, end):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] = not self.array[x][y]

line_re = re.compile(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")

def findCommandAndCoords(line):
    for command in commands:
        if command in line:
            subgrid = line.replace(command + " ", "").replace("\n", "")

            coordsInString = subgrid.split(" through ")
            # print(coordsInString)
            coords = []
            for coord in coordsInString:
                coords.append(coord.split(","))

            for i in range(len(coords)):
                coords[i] = [int(coords[i][j]) for j in range(2)]
            # print(command, coords)
            return command, coords

commands = ["toggle", "turn on", "turn off"]

if __name__ == '__main__':
    with open(infile, "r") as fp:
        input = fp.read()

    print("Part 1")
    lights = LightArray(1000, 1000)

    for line in input.splitlines():
        command, coords = findCommandAndCoords(line)
        # m = line_re.match(line)
        # if m is None:
        #     print("skipped line '{}'".format(line))
        #     continue
        op, x0, y0, x1, y1 = command, coords[0][0], coords[0][1], coords[1][0], coords[1][1]
        # x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
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
                f.write(" " if not c else "@")
            f.write("\n")
