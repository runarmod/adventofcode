import re


def main():
    # data = open("input.txt").read().rstrip().split("\n")
    data = open("testinput.txt").read().rstrip().split("\n")
    string = 0
    code = 0
    for line in data:
        string += len(line)
        code += len(line)
        code -= 2 # Leading " and ending "
        code -= line.count("\\\"") # \"
        code -= line.count("\\x") * 3 # \x00
        code -= line.count("\\\\") # \\
    print(string - code)



if __name__ == "__main__":
    main()