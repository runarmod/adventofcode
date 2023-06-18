import math
import re
import time
import networkx


def parseLines(lines):
    return int(re.findall(r"\d+", lines[0])[0]), tuple(map(int, re.findall(r"\d+", lines[1])))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.depth, self.target = parseLines(open(filename).read().rstrip().split("\n"))

    def part1(self):
        grid = self.generate_grid(self.target[0] + 1, self.target[1] + 1)

        return sum(sum(row) for row in grid)

    def generate_grid(self, max_x, max_y):
        grid = [[0 for _ in range(max_x)] for _ in range(max_y)]
        for y in range(max_y):
            grid[y][0] = y * 48271

        for x in range(max_x):
            grid[0][x] = x * 16807

        for y in range(1, max_y):
            for x in range(1, max_x):
                grid[y][x] = (
                    (grid[y][x - 1] + self.depth)
                    * (grid[y - 1][x] + self.depth)
                    % math.lcm(20183, 3)
                )

        grid[self.target[1]][self.target[0]] = 0

        for y in range(max_y):
            for x in range(max_x):
                grid[y][x] = (grid[y][x] + self.depth) % 20183 % 3

        return grid

    def get_new_coords(self, x, y):
        for dy, dx in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid)):
                continue
            yield nx, ny

    def part2(self):
        # Wild guess that we won't go more than 25 steps out of the range (can be increased if needed)
        self.grid = self.generate_grid(self.target[0] + 25, self.target[1] + 25)
        rocky, wet, narrow = range(3)
        torch, gear, neither = range(3)

        region_items = {rocky: (torch, gear), wet: (gear, neither), narrow: (torch, neither)}

        graph = networkx.Graph()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                items = region_items[self.grid[y][x]]
                graph.add_edge((x, y, items[0]), (x, y, items[1]), weight=7)
                for nx, ny in self.get_new_coords(x, y):
                    new = region_items[self.grid[ny][nx]]
                    for item in set(items).intersection(set(new)):
                        graph.add_edge((x, y, item), (nx, ny, item), weight=1)
        return networkx.dijkstra_path_length(graph, (0, 0, torch), (*self.target, torch))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
