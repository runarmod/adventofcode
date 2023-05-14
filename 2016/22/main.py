import itertools
import re
from collections import deque
import time


def parseLine(line):
    x, y, size, used = map(
        int,
        re.findall(r"/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)", line)[0],
    )
    return x, y, size, used


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = tuple(
            parseLine(line)
            for line in open(filename).read().rstrip().split("\n")[1 if self.test else 2 :]
        )

    def part1(self):
        s = 0
        for (_, _, asize, aused), (_, _, bsize, bused) in itertools.combinations(self.data, 2):
            if 0 < aused < bsize - bused:
                s += 1
            if 0 < bused < asize - aused:
                s += 1
        return s

    def data_to_map(self, data_dict):
        out = []
        x_max, y_max = (
            max(data_dict.keys(), key=lambda x: x[0])[0],
            max(data_dict.keys(), key=lambda x: x[1])[1],
        )

        top_right = (x_max, 0)
        for y in range(y_max + 1):
            new_row = []
            for x in range(x_max + 1):
                _, used = data_dict[x, y]
                if used == 0:
                    value = 0
                elif used >= 100 or self.test and used >= 25:
                    value = 2
                elif (x, y) == top_right:
                    value = -1
                else:
                    value = 1
                new_row.append(value)
            out.append(tuple(new_row))
        return tuple(out)

    def available_directions(self, grid, x, y):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for dx, dy in directions:
            if 0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[0]) and grid[y + dy][x + dx] != 2:
                yield dx, dy

    def bfs(self):
        data_dict = {(x, y): (size, used) for x, y, size, used in self.data}
        goal = (max(self.data, key=lambda x: x[0])[0], 0)
        coords_0 = next((x, y) for x, y, _, used in self.data if used == 0)

        states_visited = set()  # grid
        grid = self.data_to_map(data_dict)

        q = deque([(grid, coords_0, goal, 0)])

        while q:
            grid, coords_0, goal, steps = q.popleft()
            if goal == (0, 0):
                return steps
            if grid in states_visited:
                continue
            states_visited.add(grid)

            for dx, dy in self.available_directions(grid, *coords_0):
                new_0 = coords_0[0] + dx, coords_0[1] + dy
                new_goal = coords_0 if grid[new_0[1]][new_0[0]] == -1 else goal
                # 15x optimization. The goal never has to leave the top row
                if new_goal[1] != 0:
                    continue
                grid_lst = [list(row) for row in grid]

                # Swap 0 and another node (1 or the goal)
                grid_lst[coords_0[1]][coords_0[0]], grid_lst[new_0[1]][new_0[0]] = (
                    grid_lst[new_0[1]][new_0[0]],
                    grid_lst[coords_0[1]][coords_0[0]],
                )
                q.append((tuple((tuple(row) for row in grid_lst)), new_0, new_goal, steps + 1))

        return None

    def part2(self):
        return self.bfs()


def main():
    start = time.perf_counter()
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Total time: {time.perf_counter() - start :.4f} sec")


if __name__ == "__main__":
    main()
