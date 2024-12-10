import re
import time
from collections import deque

from aoc_utils_runarmod import get_data


def parseLines(lines):
    return [parseNumbers(line) for line in lines]


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 10) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )
        self.starts = []
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                if char == "0":
                    self.starts.append((x, y))

        self.data = parseLines(data)

    def run(self, part):
        s = 0
        for x, y in self.starts:
            ends = list()
            queue = deque([(x, y)])
            while queue:
                x, y = queue.popleft()
                for nx, ny in neighbors4_inside(
                    (x, y), (len(self.data), len(self.data[0]))
                ):
                    if self.data[ny][nx] - 1 == self.data[y][x]:
                        if self.data[ny][nx] == 9:
                            ends.append((nx, ny))
                        queue.append((nx, ny))
            if part == 1:
                s += len(set(ends))
            elif part == 2:
                s += len(ends)
            else:
                assert False
        return s

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 36 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 81 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


def neighbors4_inside(point: tuple[int, ...], dim_size: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            if 0 <= point[i] + diff < dim_size[i]:
                yield point[:i] + (point[i] + diff,) + point[i + 1 :]


if __name__ == "__main__":
    main()
