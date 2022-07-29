with open("../input.txt", "r") as f:
    directions = f.read()

allVisitedCoords = [[0, 0]]

x = y =  0

uniqueHouses = 1

for direction in directions:
    if direction == ">":
        x += 1
    elif direction == "v":
        y += 1
    elif direction == "<":
        x -= 1
    else:
        y -= 1
    coords = [x, y]
    if coords in allVisitedCoords:
        continue
    else:
        allVisitedCoords.append(coords)
        uniqueHouses += 1

print(uniqueHouses)