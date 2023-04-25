import functools
import itertools
from collections import Counter


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = sorted([0] + [int(line) for line in open(filename).read().rstrip().split("\n")])
        self.data += [max(self.data) + 3]

    def part1(self):
        counter = Counter()
        for a, b in itertools.pairwise(self.data):
            counter[b - a] += 1
        return counter[1] * counter[3]

    @functools.lru_cache(maxsize=None)
    def ways(self, index):
        s = sum(
            self.ways(new_index)
            for new_index in range(index + 1, min(index + 4, len(self.data)))
            if abs(self.data[new_index] - self.data[index]) <= 3
        )
        return 1 if index == len(self.data) - 1 else s

    def part2(self):
        return self.ways(0)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
