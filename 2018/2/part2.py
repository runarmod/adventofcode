import difflib
import itertools

def main():
    data = open("input.txt").read().rstrip().split("\n")
    # data = open("testinput.txt").read().rstrip().split("\n")
    for r in itertools.combinations(data, 2): 
        differences = [li for li in difflib.ndiff(r[0], r[1]) if li[0] != ' ']

        numdiff = len(differences) // 2
        if numdiff > 1 or numdiff == 0:
            continue
        
        s = r[0].replace(differences[0][-1], "")
        print(s)


if __name__ == "__main__":
    main()