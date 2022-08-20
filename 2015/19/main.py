from collections import defaultdict
from random import shuffle
import re
import timeit


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        pattern_rules = re.compile(r"(\w+) => (\w+)")
        self.rules = defaultdict(list)
        self.mol = "CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF"
        with open(filename) as f:
            s = f.read().rstrip()
            for match in pattern_rules.findall(s):
                self.rules[match[0]].append(match[1])
            self.list = s.split("\n")[-1]

        self.list = self.split_upper()

    def split_upper(self):
        tmp = 0
        l = []
        first = True
        for i in range(len(self.list)):
            if self.list[i].isupper() and not first:
                l.append(self.list[tmp:i])
                tmp = i
            first = False
        l.append(self.list[tmp:])
        return l

    def part1(self):
        unique = set()
        for i, atom in enumerate(self.list):
            for new in self.rules[atom]:
                unique.add("".join(self.list[:i] + [new] + self.list[i + 1 :]))
        return len(unique)

    def part2(self):
        rules = [
            ("Al", "ThF"),
            ("Al", "ThRnFAr"),
            ("B", "BCa"),
            ("B", "TiB"),
            ("B", "TiRnFAr"),
            ("Ca", "CaCa"),
            ("Ca", "PB"),
            ("Ca", "PRnFAr"),
            ("Ca", "SiRnFYFAr"),
            ("Ca", "SiRnMgAr"),
            ("Ca", "SiTh"),
            ("F", "CaF"),
            ("F", "PMg"),
            ("F", "SiAl"),
            ("H", "CRnAlAr"),
            ("H", "CRnFYFYFAr"),
            ("H", "CRnFYMgAr"),
            ("H", "CRnMgYFAr"),
            ("H", "HCa"),
            ("H", "NRnFYFAr"),
            ("H", "NRnMgAr"),
            ("H", "NTh"),
            ("H", "OB"),
            ("H", "ORnFAr"),
            ("Mg", "BF"),
            ("Mg", "TiMg"),
            ("N", "CRnFAr"),
            ("N", "HSi"),
            ("O", "CRnFYFAr"),
            ("O", "CRnMgAr"),
            ("O", "HP"),
            ("O", "NRnFAr"),
            ("O", "OTi"),
            ("P", "CaP"),
            ("P", "PTi"),
            ("P", "SiRnFAr"),
            ("Si", "CaSi"),
            ("Th", "ThCa"),
            ("Ti", "BP"),
            ("Ti", "TiTi"),
            ("e", "HF"),
            ("e", "NAl"),
            ("e", "OMg"),
        ]

        target = self.mol
        res = 0

        while target != "e":
            tmp = target

            for a, b in rules:
                res += target.count(b)
                target = target.replace(b, a)

            if tmp == target:
                target = self.mol
                res = 0
                shuffle(rules)
        return res


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
