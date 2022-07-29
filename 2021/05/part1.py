import re


# Create a dictionary keeping track of every used coordinate.
used = {}


def main():
    data = [e.replace(" -> ", ",") for e in open("input.txt").read().rstrip().split("\n")]
    # data = open("testinput.txt").read().rstrip().split("\n")
    
    # Loop thru the data and split on "," and make every element an integer.
    for i in range(len(data)):
        data[i] = [int(e) for e in data[i].split(",")]


    for line in data:
        # If index 0 and 2 are not the same, and index 1 and 3 are not the same, continue.
        if line[0] != line[2] and line[1] != line[3]:
            continue
        
        addToDictionary(line)

    # Loop thru the dictionary and count how many values are more than 1.
    count = sum(used[i] > 1 for i in used)
    print(count)
        

def addToDictionary(line):
    # If the line is horizontal, add the line to the dictionary.
    if line[0] == line[2]:
        for i in range(line[1], line[3] + (1 if line[1] < line[3] else -1), 1 if line[1] < line[3] else -1):
            # If coordinate is in the dictionary, add 1 to the value. Else create the coordinate and set the value to 1.
            if (line[0], i) in used:
                used[(line[0], i)] += 1
            else:
                used[(line[0], i)] = 1
    # If the line is vertical, add the line to the dictionary.
    elif line[1] == line[3]:
        for i in range(line[0], line[2] + (1 if line[0] < line[2] else -1), 1 if line[0] < line[2] else -1):
            # If coordinate is in the dictionary, add 1 to the value. Else create the coordinate and set the value to 1.
            if (i, line[1]) in used:
                # print((i, line[1]))
                used[(i, line[1])] += 1
            else:
                used[(i, line[1])] = 1

if __name__ == "__main__":
    main()