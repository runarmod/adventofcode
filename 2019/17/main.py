import itertools
import time
from pprint import pprint

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))
        computer = IntcodeComputer(self.data)
        self.map = ""
        for v in computer.iter():
            self.map += chr(v)
        self.map = self.map.strip().split("\n")

    def neighbours(self, x, y, grid):
        for dx, dy in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid):
                yield x + dx, y + dy

    def part1(self):
        s = 0
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell != "#":
                    continue
                if (
                    sum(
                        self.map[ny][nx] == "#"
                        for nx, ny in self.neighbours(x, y, self.map)
                    )
                    < 3
                ):
                    continue
                s += x * y
        return s

    def find_correct_dir(self, x, y, prev):
        for nx, ny in self.neighbours(x, y, self.map):
            if self.map[ny][nx] != "#":
                continue
            if nx > x and prev == "<":
                continue
            if nx < x and prev == ">":
                continue
            if ny > y and prev == "^":
                continue
            if ny < y and prev == "v":
                continue
            direction = None
            if nx > x:
                direction = ">"
            elif nx < x:
                direction = "<"
            elif ny > y:
                direction = "v"
            elif ny < y:
                direction = "^"
            return (nx, ny), direction
        return None, None

    def dir_to_rot(self, prev, next):
        if prev == "^":
            if next == ">":
                return "R"
            if next == "<":
                return "L"
        if prev == "v":
            if next == ">":
                return "L"
            if next == "<":
                return "R"
        if prev == ">":
            if next == "^":
                return "L"
            if next == "v":
                return "R"
        if prev == "<":
            if next == "^":
                return "R"
            if next == "v":
                return "L"

    def part2(self):
        start = None
        direction = None
        for x, y in itertools.product(range(len(self.map[0])), range(len(self.map))):
            if self.map[y][x] in ">v<^":
                start = (x, y)
                direction = self.map[y][x]

        path = []
        x, y = start
        while True:
            prev_dir = direction
            next_c, direction = self.find_correct_dir(x, y, direction)
            if next_c is None:
                break
            path.append(self.dir_to_rot(prev_dir, direction))
            dx, dy = next_c[0] - x, next_c[1] - y
            c = 0
            while (
                0 <= x + dx < len(self.map[0])
                and 0 <= y + dy < len(self.map)
                and self.map[y + dy][x + dx] == "#"
            ):
                c += 1
                x += dx
                y += dy
            path.append(str(c))

        s = ",".join(path)
        # Found these manually :((
        A = "L,12,L,8,L,8"
        B = "R,4,L,12,L,12,R,6"
        C = "L,12,R,4,L,12,R,6"
        s = s.replace(A, "A")
        s = s.replace(B, "B")
        s = s.replace(C, "C")

        # print(f"{A=}")
        # print(f"{B=}")
        # print(f"{C=}")
        computer = IntcodeComputer(self.data)
        computer.replace(0, 2)
        computer.inputs.extend(map(ord, s + "\n"))
        computer.inputs.extend(map(ord, A + "\n"))
        computer.inputs.extend(map(ord, B + "\n"))
        computer.inputs.extend(map(ord, C + "\n"))
        computer.inputs.extend(map(ord, "n\n"))

        while not computer.halted:
            v = computer.run()
            if v is None:
                break
            if v > 255:
                return v
            # print(chr(v), end="")

        return None


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
