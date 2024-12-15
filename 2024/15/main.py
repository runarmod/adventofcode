import itertools
import time
from collections import deque

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 15) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n\n")
        )
        self.moves = data[1].replace("\n", "")

        grid = data[0].split("\n")
        self.grids = {}

        # Grid for part 1
        self.grids[1] = []
        for y, line in enumerate(grid):
            new_line = []
            for x, c in enumerate(line):
                if c == "@":
                    self.robot = (x, y)
                    new_line.append(".")
                else:
                    new_line.append(c)
            self.grids[1].append(new_line)

        # Grid for part 2. Scaled 2x in x-direction
        self.grids[2] = []
        for y, line in enumerate(grid):
            new_line = []
            for x, c in enumerate(line):
                if c == "@":
                    # We know the position of the robot already
                    new_line.append(".")
                    new_line.append(".")
                elif c == "O":
                    new_line.append("[")
                    new_line.append("]")
                else:
                    new_line.append(c)
                    new_line.append(c)
            self.grids[2].append(new_line)

        self.H = len(self.grids[1])
        self.W = len(self.grids[1][0])

    def do_move(self, move: str, robot: tuple[int, int], part: int):
        dx, dy = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}[move]
        x, y = robot[0] + dx, robot[1] + dy
        if self.grids[part][y][x] == "#":
            return robot
        if self.grids[part][y][x] == ".":
            return (x, y)  # simply move to the new position

        lanterfishes = set()
        q = deque([])
        q.append((x, y))
        if self.grids[part][y][x] == "[":
            q.append((x + 1, y))
        if self.grids[part][y][x] == "]":
            q.append((x - 1, y))
        while q:
            x, y = q.popleft()
            if (x, y) in lanterfishes:
                continue
            lanterfishes.add((x, y))
            xx, yy = x + dx, y + dy
            if self.grids[part][yy][xx] == "#":
                return robot  # hit a wall, moving is not possible
            if self.grids[part][yy][xx] == "O":
                q.append((xx, yy))
            elif self.grids[part][yy][xx] == "[":
                q.append((xx, yy))
                q.append(
                    (xx + 1, yy)
                )  # make sure to move both sides of the lanternfish
            elif self.grids[part][yy][xx] == "]":
                q.append((xx, yy))
                q.append(
                    (xx - 1, yy)
                )  # make sure to move both sides of the lanternfish
        while len(lanterfishes):
            # move all laternfish, without overwriting each other
            for x, y in list(lanterfishes):
                xx, yy = x + dx, y + dy
                if (xx, yy) not in lanterfishes:  # Safe to move
                    self.grids[part][yy][xx], self.grids[part][y][x] = (
                        self.grids[part][y][x],
                        self.grids[part][yy][xx],
                    )
                    lanterfishes.remove((x, y))
        return robot[0] + dx, robot[1] + dy

    def visualize(self, robot: tuple[int, int], part: int):
        for y, line in enumerate(self.grids[part]):
            for x, c in enumerate(line):
                if (x, y) == robot:
                    print("@", end="")
                else:
                    print(c, end="")
            print()

    def score(self, part: int):
        s = 0
        for x, y in itertools.product(range(self.W * part), range(self.H)):
            if self.grids[part][y][x] in "[O":
                s += y * 100 + x
        return s

    def run(self, part: int):
        robot = self.robot
        if part == 2:
            robot = robot[0] * 2, robot[1]
        for move in self.moves:
            robot = self.do_move(move, robot, part)
        return self.score(part)

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 10092 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 9021 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
