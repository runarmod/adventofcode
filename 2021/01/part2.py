def main():
    data = [int(i) for i in open("input.txt").read().rstrip().split("\n")]

    newdata = [sum(data[i:i+3]) for i in range(len(data) - 2)]
    print(newdata)

    increses = 0
    prev = newdata[0]
    for line in newdata:
        if line > prev:
            increses += 1
        prev = line

    print(increses)
    # data = open("testinput.txt").read().rstrip().split("\n")



if __name__ == "__main__":
    main()