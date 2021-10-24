
def main():
    data = open("input.txt").read().rstrip().split("\n")
    dobbles = 0
    triples = 0
    for line in data:
        dobble = False
        tripple = False
        for c in list(set(line)):
            if dobble and tripple:
                break
            if line.count(c) == 2:
                dobble = True
            elif line.count(c) == 3:
                tripple = True
        dobbles += 1 if dobble else 0
        triples += 1 if tripple else 0
    print(dobbles * triples)


if __name__ == "__main__":
    main()