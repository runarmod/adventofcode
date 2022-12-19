from collections import defaultdict
from pprint import pprint
import itertools
import time
import pyperclip
import re
import string

start_x, end_x, start_y, end_y, start_y_temp, end_y_temp = 0, 0, 0, 0, 0, 0


def parseLine(line):
    global start_x, end_x, start_y, end_y, start_y_temp, end_y_temp
    if "S" in line:
        start_x = line.index("S")
        start_y = start_y_temp
        line = line.replace("S", "a")
    if "E" in line:
        end_x = line.index("E")
        end_y = end_y_temp
        line = line.replace("E", "z")
    start_y_temp += 1
    end_y_temp += 1
    return [ord(x) - ord("a") for x in line]


class Solution:
    def __init__(self, test=False):
        global start_x, end_x, start_y, end_y, start_y_temp, end_y_temp
        start_x, end_x, start_y, end_y, start_y_temp, end_y_temp = 0, 0, 0, 0, 0, 0
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    # def bfs(self, grid, x, y, end, steps, visited=set()):

    def print_visited(self, visited):
        time.sleep(0.01)
        print("\n" * 100)
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if (x, y) in visited:
                    print(str(self.data[y][x])[-1], end="")
                else:
                    print(" ", end="")
            print()

    def dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    
    def part1(self):
        global start_x, start_y, end_x, end_y
        start, end = [start_x, start_y], [end_x, end_y]
        # print(start, end)
        # if [x, y] == end:
        #     return steps

        # if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        #     return float("inf")
        # if (x, y) in visited:
        #     return float("inf")
        # if grid[y][x] not in (steps, steps - 1):
        #     return float("inf")

        visited = set()

        # length = float("inf")
        DIR = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        steps = 0
        stack = [(start, 0, 0)]
        while stack:
            pos, steps, val = stack.pop(0)
            x, y = pos
            # print([x, y], end)
            if x < 0 or y < 0 or x >= len(self.data[0]) or y >= len(self.data):
                continue
            if (x, y) in visited:
                continue
            if self.data[y][x] not in (val, val + 1):
                continue
            if self.dist([x, y], end) < 9:
                print(f"{[x, y]=}, {end=}, {self.data[y][x]=}")
            if [x, y] == end:
                print("YO")
                return steps
            # print(y,x)
            visited.add((x, y))
            # self.print_visited(visited)

            stack.extend(((x + x_change, y + y_change), steps + 1, self.data[y][x]) for x_change, y_change in DIR)

        # return steps

    def part2(self):
        return None


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    # print(solution.data)
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    copy_answer(part1, part2)

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


def copy_answer(part1, part2):
    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)


if __name__ == "__main__":
    main()
