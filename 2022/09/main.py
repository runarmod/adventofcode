import re
from typing import Dict, List, Tuple
import pyperclip


def parseLine(line):
    direction, length = re.findall(r"(R|U|D|L) (\d+)", line)[0]
    return str(direction), int(length)


DIRECTIONS: Dict[str, Tuple[int, int]] = {
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
}


class Solution:
    def __init__(self, test=False) -> None:
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def too_far_away(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> bool:
        return any((abs(coord1[0] - coord2[0]) > 1, abs(coord1[1] - coord2[1]) > 1))

    def part1(self):
        return self.rope_drag(2)

    def part2(self):
        return self.rope_drag(10)

    def rope_drag(self, n: int) -> int:
        visited = {(0, 0)}
        nodes = [[0, 0] for _ in range(n)]
        for direction, length in self.data:
            for _ in range(length):
                self.update_head(nodes, direction)
                self.update_children(nodes)
                visited.add(tuple(nodes[-1]))
        return len(visited)

    def update_head(self, nodes: List[List[int]], direction: str):
        nodes[0][0] += DIRECTIONS[direction][0]
        nodes[0][1] += DIRECTIONS[direction][1]

    def update_children(self, nodes):
        for i in range(1, len(nodes)):
            if self.too_far_away(nodes[i - 1], nodes[i]):
                self.update_child(nodes, i)

    def update_child(self, nodes, i):
        if nodes[i - 1][1] > nodes[i][1]:
            nodes[i][1] += 1
        elif nodes[i - 1][1] < nodes[i][1]:
            nodes[i][1] -= 1
        if nodes[i - 1][0] > nodes[i][0]:
            nodes[i][0] += 1
        elif nodes[i - 1][0] < nodes[i][0]:
            nodes[i][0] -= 1


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


if __name__ == "__main__":
    main()
