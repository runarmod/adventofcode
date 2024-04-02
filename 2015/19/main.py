import re
from collections import defaultdict
from random import shuffle


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.rules = defaultdict(list)
        with open(filename) as f:
            s = f.read().rstrip()
            for atom, molecule in re.findall(r"(\w+) => (\w+)", s):
                self.rules[atom].append(molecule)
            self.mol = s.split("\n\n")[-1]

        self.list = self.split_upper(self.mol)

    def split_upper(self, mol):
        return list(re.findall(r"[A-Z][a-z]*", mol))

    def part1(self):
        unique = set()
        for i, atom in enumerate(self.list):
            for new in self.rules[atom]:
                unique.add("".join(self.list[:i] + [new] + self.list[i + 1 :]))
        return len(unique)

    def part2(self):
        rules = [
            (atom, molecule)
            for atom, molecules in self.rules.items()
            for molecule in molecules
        ]
        target = self.mol
        res = 0

        while target != "e":
            tmp = target

            for atom, molecule in rules:
                res += target.count(molecule)
                target = target.replace(molecule, atom)

            if tmp == target:
                # No change
                target = self.mol
                res = 0
                shuffle(rules)
        return res


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
