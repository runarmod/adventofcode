with open("../input.txt", "r") as f:
    lines = f.read().split("\n\n")
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", " ")

valid = 0

for line in lines:
    if line.count(":") == 8:
        valid += 1
    elif "cid" not in line and line.count(":") == 7:
        valid += 1
    

print(valid)

