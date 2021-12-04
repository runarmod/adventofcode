def main():
    data = [line.split(" ") for line in open("input.txt").read().rstrip().split("\n")]
    # data = open("testinput.txt").read().rstrip().split("\n")

    x = depth = aim = 0

    for line in data:
        value = int(line[1])
        if line[0] == "forward":
            x += value
            depth += aim * value
        elif line[0] == "down":
            aim += value
        elif line[0] == "up":
            aim -= value
        else:
            raise Exception("Wrong argument", line[0])
    print(f"{x=}, {depth=}, {depth*x=}")



if __name__ == "__main__":
    main()