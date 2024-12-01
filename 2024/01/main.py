import itertools
import re
import time


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        with open(filename) as f:
            data = f.read().rstrip()

        self.data = parseNumbers(data)
        self.list1, self.list2 = zip(*list(itertools.batched(self.data, 2)))

    def part1(self):
        return sum(
            abs(val1 - val2)
            for val1, val2 in zip(sorted(self.list1), sorted(self.list2))
        )

    def part2(self):
        return sum(sum(1 for x in self.list2 if x == num) * num for num in self.list1)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 11 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 31 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
