import re
from collections import defaultdict
from itertools import permutations


class Solution():
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.raw = open(filename).read().rstrip()
        self.pattern = re.compile(
            r"(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+)\.")
        self.matches = self.pattern.findall(self.raw)
        self.names = set()
        self.happiness = defaultdict(dict)

        self.get_combinations()

        self.happinessesWithoutSelf = [self.get_happiness(
            perm) for perm in permutations(self.names)]

        # Adding myself
        self.add_myself()

        self.happinessesWithSelf = [self.get_happiness(
            perm) for perm in permutations(self.names)]

    def add_myself(self):
        for name in self.names:
            self.happiness["me"][name] = self.happiness[name]["me"] = 0
        self.names.add("me")

    def get_happiness(self, perm):
        happiness = 0
        for i in range(len(perm)):
            happiness += self.happiness[perm[i]][perm[(i + 1) % len(perm)]]
            happiness += self.happiness[perm[i]][perm[(i - 1) % len(perm)]]
        return happiness

    def get_combinations(self):
        for match in self.matches:
            name1 = match[0]
            self.names.add(name1)
            name2 = match[3]
            self.names.add(name2)
            self.happiness[name1][name2] = int(
                match[2]) * (-1 if match[1] == "lose" else 1)

    def part1(self):
        return max(self.happinessesWithoutSelf)

    def part2(self):
        return max(self.happinessesWithSelf)


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
