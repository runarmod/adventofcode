counter = 0
with open("../input.txt", "r") as f:
    inputt = f.read()

for c in inputt:
    if c == "(":
        counter += 1
    elif c == ")":
        counter -= 1

print(counter)