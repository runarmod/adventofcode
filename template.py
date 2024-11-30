import functools
import heapq
import itertools
import os
import re
import string
import sys
import time
from collections import defaultdict, deque
from pprint import pprint

import networkx as nx
from aoc_utils_runarmod import copy_answer, request_submit, write_solution
from more_itertools import (
    collapse,  # flatten all levels of nested iterables
    consume,  # exhaust an iterable
    distinct_combinations,  # distinct combinations of elements from an iterable
    distinct_permutations,  # distinct permutations of elements from an iterable
    islice_extended,  # extended slicing capabilities (islice with [::] and negative indices)
    mark_ends,  # mark the first and last element of an iterable ((is_first, is_last, val), (is_first, is_last, val), ...)
    minmax,  # find the minimum and maximum of an iterable (same as lambda x: (min(x), max(x)))
    peekable,  # peek ahead in an iterable
    sliding_window,  # return a sliding window of an iterable
    time_limited,  # time-limited execution of a function
)


def parseLine(line):
    return line


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        return None

    def part2(self):
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == None else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == None else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit("CHANGE_YEAR", "CHANGE_DATE", part1, part2)


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield point[:i] + (point[i] + diff,) + point[i + 1 :]


def neighbors8(point: tuple[int, ...], jump=1):
    for diff in itertools.product((-jump, 0, jump), repeat=len(point)):
        if any(diff):
            yield tuple(point[i] + diff[i] for i in range(len(point)))


def manhattan(p1: tuple[int, ...], p2: tuple[int, ...]):
    return sum(abs(a - b) for a, b in zip(p1, p2))


if __name__ == "__main__":
    main()
