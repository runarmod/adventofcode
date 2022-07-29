from sys import exit


with open("../input.txt", "r") as f:
    lines = f.readlines()

lines = [int(i) for i in lines]

for line in lines:
    for secondline in lines:
        for thirdsline in lines:
            if thirdsline + secondline + line == 2020:
                print(line, secondline, thirdsline)
                print(line * secondline * thirdsline)
                exit()