def main():
    data = [int(i) for i in open("input.txt").read().rstrip().split("\n")]
    

    increses = 0
    prev = data[0]
    for line in data:
        if line > prev:
            increses += 1
        prev = line

    print(increses)
    # data = open("testinput.txt").read().rstrip().split("\n")



if __name__ == "__main__":
    main()