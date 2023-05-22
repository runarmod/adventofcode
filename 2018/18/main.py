import itertools
import time


def parseData(lines):
    trees = set()
    opn = set()
    lumber = set()
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case ".":
                    opn.add((x, y))
                case "#":
                    lumber.add((x, y))
                case "|":
                    trees.add((x, y))
    return trees, opn, lumber, max_x, max_y


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.trees, self.opn, self.lumber, self.max_x, self.max_y = parseData(
            open(filename).read().rstrip().split("\n")
        )

    def iteration(self, lumber, opn, trees):
        new_trees = set()
        new_lumber = set()
        new_opn = set()

        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                trees_count = lumber_count = opn_count = 0

                for dx, dy in itertools.product(range(-1, 2), repeat=2):
                    if dx == dy == 0:
                        continue
                    trees_count += (x + dx, y + dy) in trees
                    opn_count += (x + dx, y + dy) in opn
                    lumber_count += (x + dx, y + dy) in lumber

                if (x, y) in opn:
                    if trees_count >= 3:
                        new_trees.add((x, y))
                    else:
                        new_opn.add((x, y))
                elif (x, y) in trees:
                    if lumber_count >= 3:
                        new_lumber.add((x, y))
                    else:
                        new_trees.add((x, y))
                elif (x, y) in lumber:
                    if lumber_count >= 1 and trees_count >= 1:
                        new_lumber.add((x, y))
                    else:
                        new_opn.add((x, y))
                else:
                    raise ValueError("Not in anything")

        return new_lumber, new_opn, new_trees

    def run(self, max_minutes):
        lumber, opn, trees = self.lumber, self.opn, self.trees

        seen = {}
        i = 0
        while i < max_minutes:
            lumber, opn, trees = self.iteration(lumber, opn, trees)
            state = frozenset(lumber), frozenset(opn), frozenset(trees)
            if state in seen:
                periode = i - seen[state]
                i = max_minutes - (max_minutes - i) % periode
            seen[state] = i
            i += 1
        return len(trees) * len(lumber)

    def part1(self):
        return self.run(10)

    def part2(self):
        return self.run(1000000000)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
