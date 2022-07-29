def main():
    # data = open("input.txt").read().rstrip().split("\n")
    data = open("testinput.txt").read().rstrip().split("\n")
    oxygen = co2 = ""
    first = True
    for i in range(len(data[0])):
        zeroes = ones = 0
        for j in range(len(data)):
            if first:
                continue
            elif not data[j][i].startswith(mostCommonOnesZeroes):
                break
            if data[j][i] == "0":
                zeroes += 1
            else:
                ones += 1
        first = False
        mostCommonOnesZeroes = "0" if zeroes >= ones else "1"
        oxygen += mostCommonOnesZeroes

    first = True
    for i in range(len(data[0])):
        zeroes = ones = 0
        for j in range(len(data)):
            if first:
                continue
            elif not data[j][i].startswith(leastCommonOnesZeroes):
                break
            if data[j][i] == "0":
                zeroes += 1
            else:
                ones += 1
        first = False
        leastCommonOnesZeroes = "1" if zeroes > ones else "0"
        co2 += leastCommonOnesZeroes
    print(oxygen)
    print(co2)
    print(int(oxygen, 2) * int(co2, 2))



if __name__ == "__main__":
    main()