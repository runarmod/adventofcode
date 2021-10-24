lines = open("input.txt").read().split("\n")

mem = {}
mask = "X"*36
summ = 0

for line in lines:
    if "mask" in line:
        mask = line.split(" ")[-1]
        continue
    value = int(line.split(" ")[-1])
    binaryValue = list(bin(value).replace("0b","").zfill(36))
    for i, v in enumerate(mask):
        if v == "X":
            continue
        binaryValue[i] = v

    memPos = int(line.split("[")[1].split("]")[0])
    
    result = int("".join(binaryValue),2)
    mem[memPos] = result

for v in mem:
    summ += mem[v]

print(mem)
print()
print(summ)