
lines =  open("../input.txt").read().splitlines()

seatIDs = []
for line in lines:
    i = []
    for c in line:
        if c == "B" or c == "R":
            i.append(1)
        elif c == "F" or c == "L":
            i.append(0)
    row = i[0] * 64 + i[1] * 32 + i[2] * 16 + i[3] * 8 + i[4] * 4 + i[5] * 2 + i[6]
    column = i[7] * 4 + i[8] * 2 + i[9]
    seatID = row * 8 + column
    seatIDs.append(seatID)

seatIDs.sort()
print(seatIDs)
