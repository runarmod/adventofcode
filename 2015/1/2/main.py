counter = 0
with open("../input.txt", "r") as f:
    inputt = f.read()

for i in range(len(inputt)):
    if inputt[i] == "(":
        counter += 1
    elif inputt[i] == ")":
        counter -= 1
    if counter < 0:
        print(i + 1)
        break