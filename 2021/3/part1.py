def main():
    data = open("input.txt").read().rstrip().split("\n")
    # data = open("testinput.txt").read().rstrip().split("\n")
    gamma = epsilon = ""
    for i in range(len(data[0])):
        zeroes = ones = 0
        for j in range(len(data)):
            if data[j][i] == "0":
                zeroes += 1
            else:
                ones += 1
        gamma += "0" if zeroes > ones else "1"
        epsilon += "0" if ones > zeroes else "1"
    print(gamma)
    print(epsilon)
    print(int(gamma, 2) * int(epsilon, 2))



if __name__ == "__main__":
    main()