import re
bags = {}
counter = 0

def main():
    lines = open("../test.txt").read().replace(".","").splitlines()

    for line in lines:
        splitSpace = line.split(" ")
        name = " ".join(splitSpace[0:2])
        # if "no other bags" in line:
        #     bags[name] = 
        #     continue
        bags[name] = {}
        localbags = " ".join(splitSpace[4:]).replace(" bags", "").replace(" bag", "").split(", ")
        for v in localbags:
            num = re.match(r"\d ", v)
            if not num:
                break
            bags[name][v[2:]] = {int(num[0][0])}
    # print(bags)
    with open("out.txt", "w") as f:
        f.write(str(bags))
    # print(len(bags))
    loopBags(bags)
    print(counter)


def loopBags(dictionary):
    global counter
    if dictionary == {}:
        return
    for bag in dictionary:
        print(bag)
        if bag == "shiny gold":
            counter += 1
            return
        loopBags(bags[bag])


main()