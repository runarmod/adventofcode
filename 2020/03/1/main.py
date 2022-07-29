with open("../input.txt", "r") as f:
    lines = f.readlines()

answer = 1

for dx, dy in [[3, 1]]:
    x = 0
    trees = 0
    y = 0
    while y < len(lines) - dy:
        y += dy
        line = lines[y]
        line = line.strip()
        x += dx
        x %= len(line)
        if line[x] == "#":
            trees += 1
    answer *= trees
print("The answer is", answer)