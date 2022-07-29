
lines = open("in.txt").read().splitlines()

def part1():
    summ = 0
    for line in lines:
        largest = 0
        smallest = 999999999
        for cell in line.split("\t"):
            cell = int(cell)
            if cell < smallest:
                smallest = cell
            if cell > largest:
                largest = cell
        summ += largest - smallest
    return summ

def part2():
    summ = 0
    for line in lines:
        for i in line.split("\t"):
            i = int(i)
            for j in line.split("\t"):
                j = int(j)
                if i == j:
                    continue
                if (i / j) % 1 == 0:
                    div = i / j
                    break
        summ += div
    return int(summ)

print("Part 1:", part1())
print("Part 2:", part2())