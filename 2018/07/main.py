import functools
import itertools
import os
import re
import string
import sys
from collections import defaultdict, deque
from pprint import pprint

sys.path.insert(0, "../../")
from utils import copy_answer, request_submit, write_solution


def parseLine(line):
    return tuple(re.findall(r"tep (\w)", line))[::-1]


def toposort(graph):
    visited = [False for i in range(len(graph))]
    result = []

    def DFS(node):
        if visited[node]:
            return
        visited[node] = True
        for adj in graph[node]:
            DFS(adj)
        result.append(node)

    for i in range(len(graph)):
        DFS(i)

    return result


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]
        self.unique = tuple(sorted({frm for frm, _ in self.data}.union({to for _, to in self.data})))

        # print({frm for frm, _ in self.data}.difference({to for _, to in self.data}))
        self.start = next(
            iter({frm for frm, _ in self.data}.difference({to for _, to in self.data}))
        )

        self.dict = {frm: {to for frm2, to in self.data if frm2 == frm} for frm, _ in self.data}
        # print(self.data)
        # print(self.start)
        # print(self.dict)

        graph = [
            [0 if i not in self.dict.get(j, []) else 1 for i in self.unique] for j in self.unique
        ]
        # pprint(graph)
        
        print(toposort(graph))

    def part1(self):
        return None

    def part2(self):
        return None


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit(2018, 7, part1, part2)


if __name__ == "__main__":
    main()
