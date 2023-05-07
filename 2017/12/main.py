import re
from collections import defaultdict


def parseLine(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"(\d+)", line)))


class Solution:
    def __init__(self, test: bool = False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = map(parseLine, open(filename).read().rstrip().split("\n"))
        self.groups: defaultdict[int, set[int]] = defaultdict(set)

    def find_size(self, num: int, visited: set[int]) -> int:
        visited.add(num)
        for n in self.groups[num]:
            if n not in visited:
                self.find_size(n, visited)
        return len(visited)

    def part1(self) -> int:
        for nums in self.data:
            num, nums = nums[0], nums[1:]
            for number in nums:
                self.groups[num].add(number)

        return self.find_size(0, set())

    def part2(self) -> int:
        visited: set[int] = set()
        groups = 0
        for i in range(len(self.groups)):
            if i not in visited:
                self.find_size(i, visited)
                groups += 1
        return groups


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
