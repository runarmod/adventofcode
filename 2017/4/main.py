lines = open("in.txt").read().splitlines()

def part1():
    summ = 0
    for line in lines:
        if len(line.split(" ")) == len(list(set(line.split(" ")))):
            summ += 1
    return summ

def part2():
    summ = 0
    for line in lines:
        # nothin
        for i in range(len(line)):
            word1 = line[i]
            for j in range(len(line)):
                word2 = line[j]
                if i == j:
                    continue
                if sorted(word1) == sorted(word2):
                    summ += 1
                    goto(13)
    return summ


print("Part 1:", part1())
print("Part 2:", part2())