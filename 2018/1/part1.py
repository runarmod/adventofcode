
def main():
    data = open("./input.txt").read().rstrip().split("\n")
    out = 0
    for line in data:
        operation = line[0]
        if operation == "+":
            out += int(line[1:])
        else:
            out -= int(line[1:])
    print(out)


if __name__ == "__main__":
    main()