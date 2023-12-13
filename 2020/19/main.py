from copy import deepcopy
import re
import time


def parseLine(line):
    num, rule = line.split(": ")
    num = int(num)
    rule = rule.replace('"', "")

    if rule == "a" or rule == "b":
        return num, rule
    a = rule.split(" | ")

    return num, [list(map(int, b.split())) for b in a]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        rules, tests = open(filename).read().rstrip().split("\n\n")
        self.rules = dict([parseLine(line) for line in rules.split("\n")])
        self.tests = tests.split("\n")

    def fix_rule(self, rules, all_rules, depth=0):
        if depth > 100:
            return ""
        if isinstance(rules, str):
            return rules
        if isinstance(rules, int):
            return self.fix_rule(all_rules[rules], all_rules, depth + 1)
        if isinstance(rules, list):
            if all(isinstance(r, int) for r in rules):
                return "".join(self.fix_rule(r, all_rules, depth + 1) for r in rules)
            return (
                r"(?:"
                + "|".join(self.fix_rule(r, all_rules, depth + 1) for r in rules)
                + r")"
            )

    def part1(self):
        new_rules = deepcopy(self.rules)
        return self.run(new_rules)

    def part2(self):
        new_rules = deepcopy(self.rules)
        new_rules[8] = [[42], [42, 8]]
        new_rules[11] = [[42, 31], [42, 11, 31]]

        return self.run(new_rules)

    def run(self, new_rules):
        while not all(isinstance(v, str) for v in new_rules.values()):
            for k, v in new_rules.items():
                new_rules[k] = self.fix_rule(v, new_rules)

        regex = re.compile(new_rules[0])

        s = 0
        for test in self.tests:
            match = regex.match(test)
            if match and match.end() == len(test):
                s += 1
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 3 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 12 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
