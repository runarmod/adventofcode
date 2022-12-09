from collections import defaultdict
import itertools
import re
import string
from pprint import pprint
import pyperclip
import matplotlib.pyplot as plt


def parseLine(line):
    direction, length = re.findall(r"(R|U|D|L) (\d+)", line)[0]
    return direction, int(length)


DIRECTIONS = {
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
}


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def too_far_away(self, a, b):
        return any((abs(a[0] - b[0]) > 1, abs(a[1] - b[1]) > 1))

    def part1(self):
        visited = {(0, 0)}
        head, tail = [0, 0], [0, 0]
        for direction, length in self.data:
            for _ in range(1, length + 1):
                head = [
                    head[0] + DIRECTIONS[direction][0],
                    head[1] + DIRECTIONS[direction][1],
                ]
                if self.too_far_away(head, tail):
                    if head[0] == tail[0]:
                        tail[1] += DIRECTIONS[direction][1]
                    elif head[1] == tail[1]:
                        tail[0] += DIRECTIONS[direction][0]
                    elif head[0] > tail[0]:
                        if head[1] > tail[1]:
                            tail = [tail[0] + 1, tail[1] + 1]
                        else:
                            tail = [tail[0] + 1, tail[1] - 1]
                    elif head[1] > tail[1]:
                        tail = [tail[0] - 1, tail[1] + 1]
                    elif head[1] < tail[1]:
                        tail = [tail[0] - 1, tail[1] - 1]
                    else:
                        print("WTF")
                        raise NotImplementedError("WTF")
                visited.add(tuple(tail))
        # plt.scatter(*zip(*visited))
        # plt.show()
        return len(visited)

    def part2(self):
        visited = {(0, 0)}
        nodes = [[0, 0] for _ in range(10)]
        for direction, length in self.data:
            for _ in range(length):
                nodes[0] = [
                    nodes[0][0] + DIRECTIONS[direction][0],
                    nodes[0][1] + DIRECTIONS[direction][1],
                ]
                for i in range(1, len(nodes)):
                    if self.too_far_away(nodes[i - 1], nodes[i]):
                        if nodes[i - 1][0] == nodes[i][0]:
                            if nodes[i - 1][1] > nodes[i][1]:
                                nodes[i][1] += 1
                            elif nodes[i - 1][1] < nodes[i][1]:
                                nodes[i][1] -= 1
                            else:
                                print("WTF")
                                raise NotImplementedError("WTF")
                        elif nodes[i - 1][1] == nodes[i][1]:
                            if nodes[i - 1][0] > nodes[i][0]:
                                nodes[i][0] += 1
                            elif nodes[i - 1][0] < nodes[i][0]:
                                nodes[i][0] -= 1
                            else:
                                print("WTF")
                                raise NotImplementedError("WTF")
                        elif nodes[i - 1][0] > nodes[i][0]:
                            if nodes[i - 1][1] > nodes[i][1]:
                                nodes[i] = [nodes[i][0] + 1, nodes[i][1] + 1]
                            else:
                                nodes[i] = [nodes[i][0] + 1, nodes[i][1] - 1]
                        elif nodes[i - 1][1] > nodes[i][1]:
                            nodes[i] = [nodes[i][0] - 1, nodes[i][1] + 1]
                        elif nodes[i - 1][1] < nodes[i][1]:
                            nodes[i] = [nodes[i][0] - 1, nodes[i][1] - 1]
                        else:
                            print("WTF")
                            raise NotImplementedError("WTF")
                visited.add(tuple(nodes[-1]))

        # plt.scatter(*zip(*visited))
        # plt.show()
        return len(visited)


def main():
    test = Solution(test=True)
    print(part1_test := f"(TEST) Part 1: {test.part1()}")
    print(part2_test := f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    print(part1_text := f"Part 1: {part1}")
    part2 = solution.part2()
    print(part2_text := f"Part 2: {part2}")

    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


if __name__ == "__main__":
    main()
