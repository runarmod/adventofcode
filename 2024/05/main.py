import re
import time
from itertools import pairwise

import networkx as nx
from aoc_utils_runarmod import get_data


def parseLines(lines):
    return [parseNumbers(line) for line in lines]


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        restrictions, lists = (
            (get_data(2024, 5) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n\n")
        )

        self.restrictions = set(parseLines(restrictions.split("\n")))
        self.lists = parseLines(lists.split("\n"))
        self.incorrects: list[list[int]] = []

    def part1(self):
        s = 0
        for nums in self.lists:
            if not any(order[::-1] in self.restrictions for order in pairwise(nums)):
                s += nums[len(nums) // 2]
            else:
                # For part 2
                self.incorrects.append(nums)
        return s

    def part2(self):
        s = 0
        for nums in self.incorrects:
            graph = nx.DiGraph()
            for node1, node2 in self.restrictions:
                if node1 in nums and node2 in nums:
                    graph.add_edge(node1, node2)
            correct = list(filter(lambda x: x in nums, nx.topological_sort(graph)))
            s += correct[len(correct) // 2]
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 143 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 123 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
