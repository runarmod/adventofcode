from tqdm import tqdm
with open("../input.txt", "r") as f:
    lines = f.readlines()

valid = 0

for i, line in enumerate(tqdm(lines)):
    line.strip()
    linje = []
    line = line.split("-")
    line[1] = line[1].split(": ")
    line[1][0] = line[1][0].split()
    linje.append(int(line[0]))
    linje.append(int(line[1][0][0]))
    linje.append(line[1][0][1])
    linje.append(line[1][1])
    
    if linje[0] <= linje[3].count(linje[2]) <= linje[1]:
        valid += 1

print(valid)