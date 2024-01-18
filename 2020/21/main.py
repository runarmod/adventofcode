from collections import defaultdict
import functools
import time


def parseLine(line):
    first, second = line.rstrip(")").split(" (contains ")
    return set(first.split(" ")), set(second.split(", "))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

        self.allergens = set(
            allergen for _, allergens in self.data for allergen in allergens
        )
        self.ingredients = set(
            ingredient for ingredients, _ in self.data for ingredient in ingredients
        )

    def count_occurrences(self):
        return sum(
            1
            for ingredients, _ in self.data
            for ingredient in ingredients
            if ingredient not in self.mappings.values()
        )

    def part1(self):
        allergen_lines = defaultdict(list)
        for ingredients, allergens in self.data:
            for allergen in allergens:
                allergen_lines[allergen].append(ingredients)

        possible = defaultdict(set)
        for allergen in self.allergens:
            possible[allergen] = functools.reduce(
                lambda a, b: a & b, allergen_lines[allergen], self.ingredients
            )

        self.mappings = {}
        while len(self.mappings) < len(self.allergens):
            for allergen, ingredients in possible.items():
                if len(ingredients) == 1:
                    ingredient = ingredients.pop()
                    self.mappings[allergen] = ingredient
                    for other_ingredients in possible.values():
                        other_ingredients -= {ingredient}
                    break
        return self.count_occurrences()

    def part2(self):
        return ",".join(ingredient for _, ingredient in sorted(self.mappings.items()))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}\t\t\t{'correct :)' if test1 == 5 else 'wrong :('}")
    print(
        f"(TEST) Part 2: {test2}\t{'correct :)' if test2 == 'mxmxvkd,sqjhc,fvjkl' else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
