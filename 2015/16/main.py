from collections import defaultdict
import re

class Solution():
    def __init__(self, test=False):  # sourcery skip: use-itertools-product
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.inn = open(filename).read().rstrip()
        self.pattern = re.compile(r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)")
        self.d = tuple(tuple(int(v) if v.isdigit() else v for v in match) for match in self.pattern.findall(self.inn))
        self.data = defaultdict(dict)

        self.correct = defaultdict(dict)
        for k, v in re.findall(r"(\w+): (\d+)", open("correct.txt", "r").read().rstrip()):
            self.correct[k] = int(v)
            
        for instance in self.d:
            for i in range(1,7,2):
                self.data[instance[0]][instance[i]] = instance[i+1]


    def part1(self):
        localData = self.data.copy()
        temp = []
        for correctFocus, correctAmount in self.correct.items():
            for sueNumber, sueContent in localData.items():
                if correctFocus in sueContent and sueContent[correctFocus] != correctAmount:
                    temp.append(sueNumber)
            for i in temp:
                del localData[i]
            temp = []
        return localData.popitem()[0]

    def part2(self):
        localData = self.data.copy()
        temp = []
        for correctFocus, correctAmount in self.correct.items():
            for sueNumber, sueContent in localData.items():
                if correctFocus in ("cats", "trees"):
                    if correctFocus in sueContent and sueContent[correctFocus] <= correctAmount:
                        temp.append(sueNumber)
                elif correctFocus in ("pomeranians", "goldfish"):
                    if correctFocus in sueContent and sueContent[correctFocus] >= correctAmount:
                        temp.append(sueNumber)
                elif correctFocus in sueContent and sueContent[correctFocus] != correctAmount:
                    temp.append(sueNumber)
            for i in temp:
                del localData[i]
            temp = []
        return localData.popitem()[0]


def main():
    solution = Solution(test=False)
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
