import math

with open("input.txt", "r") as f:
    operations = f.read().splitlines()


def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

# blacks = 0
blacks = []

for o in operations:
    x = y = 0
    i = 0
    while i < len(o):
        # print(i)
        if o[i] == "e":
            x += 1
            i += 1
        elif o[i] == "w":
            x -= 1
            i += 1
        elif o[i:i+2] == "ne":
            x += 0.5
            y += 1
            i += 2
        elif o[i:i+2] == "nw":
            x -= 0.5
            y += 1
            i += 2
        elif o[i:i+2] == "se":
            x += 0.5
            y -= 1
            i += 2
        elif o[i:i+2] == "sw":
            x -= 0.5
            y -= 1
            i += 2
    # pos = blacks.index([x, y])
    if search(blacks, [x, y]):
        blacks.remove([x, y])
    else:
        blacks.append([x, y])
print(len(blacks))