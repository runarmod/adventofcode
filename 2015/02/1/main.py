paper = 0
with open("../input.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    dimentions = line.split("x")
    dimentions = [int(dimention) for dimention in dimentions]
    dimentions.sort()
    sides = [2 * dimentions[0] * dimentions[1], 2 * dimentions[0] * dimentions[2], 2 * dimentions[1] * dimentions[2]]
    for side in sides:
        paper += side
    paper += dimentions[0] * dimentions[1]

print(paper)