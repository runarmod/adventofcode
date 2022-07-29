with open("../input.txt", "r") as f:
    directions = f.read()

allVisitedCoords = [[0, 0]]

santaX = santaY = roboX = roboY = 0

uniqueHouses = 1

for i in range(len(directions)):
    if i % 2 == 0:
        if directions[i] == ">":
            santaX += 1
        elif directions[i] == "v":
            santaY += 1
        elif directions[i] == "<":
            santaX -= 1
        else:
            santaY -= 1
        coords = [santaX, santaY]
    else:
        if directions[i] == ">":
            roboX += 1
        elif directions[i] == "v":
            roboY += 1
        elif directions[i] == "<":
            roboX -= 1
        else:
            roboY -= 1
        coords = [roboX, roboY]
    if coords in allVisitedCoords:
        continue
    else:
        allVisitedCoords.append(coords)
        uniqueHouses += 1

print(uniqueHouses)