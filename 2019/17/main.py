import itertools
import time

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

    def get_substring(self, path, start_search, max_length=20, min_length=6):
        for start in range(start_search, len(path)):
            if path[start] == ",":
                continue
            for end in range(start + min_length, min(start + max_length, len(path))):
                if path[end - 1] == ",":
                    continue
                yield start, end

    def compress(self, path):
        for a_s, a_e in self.get_substring(path, 0):
            for b_s, b_e in self.get_substring(path, a_e):
                for c_s, c_e in self.get_substring(path, b_e):
                    A, B, C = (
                        path[a_s:a_e],
                        path[b_s:b_e],
                        path[c_s:c_e],
                    )
                    s = path.replace(A, "A").replace(B, "B").replace(C, "C")
                    if len(s) <= 20:
                        return s, A, B, C

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

        s, A, B, C = self.compress(",".join(path))

        computer = IntcodeComputer(self.data)
        computer.replace(0, 2)
        for x in (s, A, B, C, "n"):
            computer.inputs.extend(map(ord, x + "\n"))

        for v in computer.iter():
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
