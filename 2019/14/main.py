from collections import defaultdict, namedtuple
from toposort import toposort
import math
import time


def parseLine(line):
    a, b = line.split(" => ")
    return tuple(c.split(" ") for c in a.split(", ")), b.split(" ")


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

        dependency = namedtuple("Dependency", ["count", "ingredients"])
        self.detailed_needs = {
            result[1]: dependency(
                int(result[0]), {need[1]: int(need[0]) for need in needs}
            )
            for needs, result in self.data
        }

        needs = self.create_needing_dict()
        self.order = list(toposort(needs))

    def create_needing_dict(self):
        d = {}
        for needs, result in self.data:
            assert result[1] not in d
            d[result[1]] = {material for _, material in needs}
        return d

    def part1(self):
        return self.calc(1)

    def calc(self, fuel_count):
        needs = defaultdict(lambda: 0)
        needs["FUEL"] = fuel_count
        for section in self.order[::-1]:
            for material in section:
                if material == "ORE":
                    continue
                dependency = self.detailed_needs[material]
                required_iterations = max(
                    1, math.ceil(needs[material] / dependency.count)
                )
                for ing, count in dependency.ingredients.items():
                    needs[ing] += required_iterations * count
        return needs["ORE"]

    def part2(self):
        AVAILABLE_ORE = 1_000_000_000_000
        left, right = 1, AVAILABLE_ORE
        while left <= right:
            m = (left + right) // 2
            req = self.calc(m)
            if req == AVAILABLE_ORE:
                return m
            if req > AVAILABLE_ORE:
                right = m - 1
            else:
                left = m + 1
        return m


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1},\t{'correct :)' if test1 == 2210736 else 'wrong :('}"
    )
    print(f"(TEST) Part 2: {test2},\t{'correct :)' if test2 == 460664 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
