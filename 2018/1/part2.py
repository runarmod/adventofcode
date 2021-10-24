
def main():
    data = open("./input.txt").read().rstrip().split("\n")
    out = 0
    checked = [out]
    while True:
        for line in data:
            operation = line[0]
            if operation == "+":
                out += int(line[1:])
            else:
                out -= int(line[1:])
            if out in checked:
                print(out)
                return
            checked.append(out)

if __name__ == "__main__":
    main()