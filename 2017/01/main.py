inn = open("in.txt").read()

def part1(streng = inn):
    prev = ""
    summ = 0
    for c in streng:
        if c == prev:
            summ += int(c)
        prev = c
    if streng[0] == streng[-1]:
        summ += int(streng[0])
    return summ

def part2(streng = inn):
    i = len(streng) // 2
    summ = 0
    for c in streng:
        if c == streng[i % len(streng)]:
            summ += int(c)
        i += 1
    return summ

print("Part 1:", part1())
print("Part 2:", part2())