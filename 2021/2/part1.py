def main():
    data = [line.split(" ") for line in open("input.txt").read().rstrip().split("\n")]
    # data = open("testinput.txt").read().rstrip().split("\n")

    x = depth = 0

    for line in data:
        if line[0] == "forward":
            x += int(line[1])
        elif line[0] == "down":
            depth += int(line[1])
        elif line[0] == "up":
            depth -= int(line[1])
        else:
            raise Exception("Wrong argument", line[0])
    print(f"{x=}, {depth=}, {depth*x=}")



if __name__ == "__main__":
    main()