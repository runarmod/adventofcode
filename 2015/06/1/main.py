with open("../test.txt", "r") as f:
    lines = f.readlines()

size = 10
grid = [[0] * size] * size
commands = ["toggle", "turn on", "turn off"]

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


def countLights():
    lights = 0
    for y in range(size):
        for x in range(size):
            if grid[x][y] == 1:
                lights += 1
    return lights

for line in lines:
    command, coords = findCommandAndCoords(line)

    yStart = coords[0][1]
    yEnd = coords[1][1]
    xStart = coords[0][0]
    xEnd = coords[1][0]

    # print(yStart, yEnd)
    # print(xStart, xEnd)

    yRange = range(yStart, yEnd + 1)
    xRange = range(xStart, xEnd + 1)

    print(yRange, xRange)
    for y in yRange:
        # print(y)
        for x in xRange:
            # print(y, x, command)
            if command == commands[0]:
                if grid[x][y] == 0:
                    grid[x][y] = 1
                else:
                    grid[x][y] = 0
                # grid[x][y] = (grid[x][y] + 1) % 2
                # print(grid[x][y])
            elif command == commands[1]:
                grid[x][y] = 1
                # print(grid[x][y])
                # print(countLights())
            elif command == commands[2]:
                print(x, y)
                grid[x][y] = 0
                print(grid)
                # print(grid[x][y])
                # print(x, y)
            else:
                print(command, "is not a command")

lights = countLights()

with open("output.txt", "w") as f:
    for line in grid:
        for c in line:
            f.write(str(c))
        f.write("\n")

print(lights)
