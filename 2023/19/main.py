import functools
import re
import time


def parseLine(line):
    name, last = line[:-1].split("{")
    out = []
    for section in last.split(","):
        if ":" not in section:
            out.append(section)
            continue

        l = list(re.findall(r"(\w+)([<>])(\d+):(\w+)", section)[0])
        l[2] = int(l[2])
        out.append(l)
    return {name: out}


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        rules_section, items_section = open(filename).read().rstrip().split("\n\n")

        self.create_rules(rules_section)
        self.create_items(items_section)
        self.create_lambdas(self.rules)

    def create_rules(self, rules):
        self.rules = {}
        for line in rules.split("\n"):
            self.rules.update(parseLine(line))

    def create_items(self, items):
        self.items = []
        for line in items.split("\n"):
            line_dict = {}
            founds = re.findall(r"(\w+)=(\d+)", line)
            for letter, number in founds:
                line_dict[letter] = int(number)
            self.items.append(line_dict)

    def create_lambdas(self, rules):
        self.lambdas = {}
        for key, rule in rules.items():
            self.lambdas[key] = []
            for item in rule:
                if isinstance(item, str):
                    self.lambdas[key].append((lambda _: True, item))
                    continue

                var, sign, value, nxt = item

                if sign == "<":
                    self.lambdas[key].append(
                        (
                            (lambda k, i: (lambda x: x[k] < i))(var, value),
                            nxt,
                        )
                    )
                elif sign == ">":
                    self.lambdas[key].append(
                        (
                            (lambda k, i: (lambda x: x[k] > i))(var, value),
                            nxt,
                        )
                    )

    def get_value(self, item, rule):
        for func, nxt in self.lambdas[rule]:
            answer = func(item)
            if answer:
                if nxt in ["A", "R"]:
                    return nxt
                return self.get_value(item, nxt)
        assert False

    def part1(self):
        return sum(
            sum(item.values())
            for item in self.items
            if self.get_value(item, "in") == "A"
        )

    def calc(self, item, ranges):
        if item == "R":
            return 0

        if item == "A":
            return functools.reduce(
                lambda x, r: x * (r.stop - r.start), ranges.values(), 1
            )

        total = 0
        for rule in self.rules[item]:
            if isinstance(rule, str):
                total += self.calc(rule, ranges)
                continue

            var, sign, value, nxt = rule

            new_range = dict(ranges)

            if value in ranges[var]:
                if sign == "<":
                    new_range[var] = range(ranges[var].start, value)
                    ranges[var] = range(value, ranges[var].stop)
                else:
                    new_range[var] = range(value + 1, ranges[var].stop)
                    ranges[var] = range(ranges[var].start, value + 1)
                total += self.calc(nxt, new_range)
        return total

    def part2(self):
        return self.calc(
            "in",
            {
                "x": range(1, 4001),
                "m": range(1, 4001),
                "a": range(1, 4001),
                "s": range(1, 4001),
            },
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1},\t\t{'correct :)' if test1 == 19114 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2},\t{'correct :)' if test2 == 167409079868000 else 'wrong :('}"
    )

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")

    assert part1 == 532551, f"Answer has been changed!"
    assert part2 == 134343280273968, f"Answer has been changed!"


if __name__ == "__main__":
    main()
