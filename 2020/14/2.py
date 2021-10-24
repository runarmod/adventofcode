lines = open("input.txt").read().split("\n")

mem = {}
mask = "X"*36
summ = 0

def turnToBinaryFilled(value):
    return list(bin(value).replace("0b","").zfill(36))

for line in lines:
    if "mask" in line:
        mask = line.split(" ")[-1]
        continue
    value = int(line.split(" ")[-1])
    
    binaryValue = turnToBinaryFilled(value)
    for i, v in enumerate(mask):
        if v == "X":
            continue
        binaryValue[i] = v
    result = int("".join(binaryValue),2)

    memPos = turnToBinaryFilled(int(line.split("[")[1].split("]")[0]))

    for i, v in enumerate(mask):
        if v == "0":
            continue
        memPos[i] = v
        # result = int("".join(binaryValue),2)
    indexes = []
    inndex = 0
    memPosString = "".join(memPos)
    while True:
        indexxx = memPosString.find("X", inndex)
        if indexxx == -1: 
            break
        indexes.append(indexxx)
        inndex = indexes[-1] + 1
    # print(indexes)

    binn = 0
    for i in range(len(indexes) ** 2):
        binbinn = bin(binn).replace("0b","").zfill(len(indexes))
        # print(binbinn)
        for k, j in enumerate(indexes):
            memPos[j] = binbinn[k]
        binn += 1
        intt = int("".join(memPos),2)
        mem[intt] = value

    # mem[memPos] = result

for v in mem:
    summ += mem[v]

# print(mem)
print()
print(summ)