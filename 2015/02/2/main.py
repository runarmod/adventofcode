ribbon = 0
with open("../input.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    dimentions = line.split("x")
    dimentions = [int(dimention) for dimention in dimentions]
    dimentions.sort()
    sides = [2 * dimentions[0] * dimentions[1], 2 * dimentions[0] * dimentions[2], 2 * dimentions[1] * dimentions[2]]
    ribbon += dimentions[0] * 2 + dimentions[1] * 2 # AROUND THE PRESENT

    volume = 1
    for length in dimentions:
        volume *= length
    
    ribbon += volume

print(ribbon)