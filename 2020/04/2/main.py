import re

with open("../input.txt", "r") as f:
    lines = f.read().split("\n\n")
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", " ")

validNumber = 0

def checkByr(line):
    if re.search(r"byr:(19[2-8][0-9]|199[0-9]|200[0-2])", line):
        return True
    return False


def checkIyr(line):
    if re.search(r"iyr:(201[0-9]|2020)", line):
        return True
    return False


def checkEyr(line):
    if re.search(r"eyr:(202[0-9]|2030)", line):
        return True
    return False


def checkHgt(line):
    if re.search(r"hgt:((1[5-8][0-9]|19[0-3])cm|(5[6-9]|6[0-9]|7[0-6])in)", line):
        return True
    return False

def checkHcl(line):
    if re.search(r"hcl:#[0-9a-f]{6}", line):
        return True
    return False


def checkEcl(line):
    if re.search(r"ecl:(amb|blu|brn|gry|grn|hzl|oth)", line):
        return True
    return False


def checkPid(line):
    if re.search(r"pid:(\d){9}\b", line):
        return True
    return False


def checkCid(line):
    return True


for line in lines:
    if not checkByr(line):
        continue
    if not checkIyr(line):
        continue
    if not checkEyr(line):
        continue
    if not checkHgt(line):
        continue
    if not checkHcl(line):
        continue
    if not checkEcl(line):
        continue
    if not checkPid(line):
        continue
    if not checkCid(line):
        continue
    validNumber += 1

print(validNumber)
# print(checkPid("pid:023456789"))
