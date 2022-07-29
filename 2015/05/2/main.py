with open("../input.txt", "r") as f:
    lines = f.readlines()

numberOfNiceWords = 0


def checkPairs(line):
    for letterIndex in range(len(line)):
        if letterIndex < len(line) - 2:
            pair = line[letterIndex : letterIndex + 2]
            if line.count(pair) >= 2:
                # print(line[letterIndex : letterIndex + 2])
                # print(pair)
                return True

    return False


def checkRepeat(line):
    for letterIndex in range(len(line)):
        if letterIndex < len(line) - 3:
            if line[letterIndex] == line[letterIndex + 2]:
                return True
    return False


for line in lines:
    hasPairs = checkPairs(line)
    hasRepeat = checkRepeat(line)
    
    # print(hasPairs)

    if not hasPairs:
        continue
    if not hasRepeat:
        continue

    numberOfNiceWords += 1

print(numberOfNiceWords)