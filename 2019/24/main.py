import collections
import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")

        self.height = len(self.data)
        self.width = len(self.data[0])

        self.bugs = set()
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.bugs.add((x, y))

    def next_state(self, bugs: frozenset[tuple[int, int]]):
        new_bugs = set()
        for y in range(self.height):
            for x in range(self.width):
                count = 0
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    n_x, n_y = x + dx, y + dy
                    if (n_x, n_y) in bugs:
                        count += 1
                if (x, y) in bugs:
                    if count == 1:
                        new_bugs.add((x, y))
                else:
                    if count in (1, 2):
                        new_bugs.add((x, y))
        return frozenset(new_bugs)

    def calculate_biodiversity(self, bugs):
        return sum(2 ** (y * self.width + x) for x, y in bugs)

    def part1(self):
        bugs = frozenset(self.bugs)
        cache = {bugs: 0}
        for i in itertools.count(start=1):
            bugs = self.next_state(bugs)
            if bugs in cache:
                return self.calculate_biodiversity(bugs)
            cache[bugs] = i

    def part2_next_state(self, bugs: dict[int, set[tuple[int, int]]]):
        surrounding_bugs = collections.defaultdict(int)  # (level, (x, y)) -> count
        for level, state in bugs.items():
            for x, y in state:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    n_x, n_y = x + dx, y + dy
                    if (
                        not (n_x == 2 and n_y == 2)
                        and n_x in range(self.width)
                        and n_y in range(self.height)
                    ):
                        surrounding_bugs[level, (n_x, n_y)] += 1
                    elif n_x == -1:
                        surrounding_bugs[level - 1, (1, 2)] += 1
                    elif n_x == 5:
                        surrounding_bugs[level - 1, (3, 2)] += 1
                    elif n_y == -1:
                        surrounding_bugs[level - 1, (2, 1)] += 1
                    elif n_y == 5:
                        surrounding_bugs[level - 1, (2, 3)] += 1
                    elif n_x == 2 and n_y == 2:
                        if x == 1:
                            for i in range(5):
                                surrounding_bugs[level + 1, (0, i)] += 1
                        elif x == 3:
                            for i in range(5):
                                surrounding_bugs[level + 1, (4, i)] += 1
                        elif y == 1:
                            for i in range(5):
                                surrounding_bugs[level + 1, (i, 0)] += 1
                        elif y == 3:
                            for i in range(5):
                                surrounding_bugs[level + 1, (i, 4)] += 1
                    else:
                        raise ValueError(f"Invalid coordinates: {n_x, n_y}")

        new_bugs = collections.defaultdict(set)
        for level, (x, y) in surrounding_bugs:
            if level in bugs and (x, y) in bugs[level]:
                if surrounding_bugs[level, (x, y)] == 1:
                    new_bugs[level].add((x, y))
            elif surrounding_bugs[level, (x, y)] in (1, 2):
                new_bugs[level].add((x, y))
        return new_bugs

    def part2(self):
        bugs = {0: self.bugs}
        for _ in range(10 if self.test else 200):
            bugs = self.part2_next_state(bugs)
        return sum(len(bugs[level]) for level in bugs)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, {'correct :)' if test1 == 2129920 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 99 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
