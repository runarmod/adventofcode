from collections import deque
import sys
import time
import networkx

sys.setrecursionlimit(10**6)


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [list(line) for line in open(filename).read().rstrip().split("\n")]
        self.start_x = next(x for x, c in enumerate(self.data[0]) if c == ".")
        self.end_x = next(x for x, c in enumerate(self.data[-1]) if c == ".")

    def part1(self):
        q = deque()  # x, y, l, v
        q.append((self.start_x, 0, 0, set()))
        best = 0
        while q:
            x, y, l, v = q.popleft()
            if x == self.end_x and y == len(self.data) - 1:
                best = max(best, l)
                continue
            if (x, y) in v:
                continue
            if self.data[y][x] == ".":
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < len(self.data[0]) and 0 <= y + dy < len(self.data):
                        if self.data[y + dy][x + dx] == ".":
                            q.append((x + dx, y + dy, l + 1, v | {(x, y)}))
            if self.data[y][x + 1] == ">":  # "^><v":
                q.append((x + 2, y, l + 2, v | {(x, y), (x + 1, y)}))
            if self.data[y][x - 1] == "<":
                q.append((x - 2, y, l + 2, v | {(x, y), (x - 1, y)}))
            if self.data[y - 1][x] == "^":
                q.append((x, y - 2, l + 2, v | {(x, y), (x, y - 1)}))
            if self.data[y + 1][x] == "v":
                q.append((x, y + 2, l + 2, v | {(x, y), (x, y + 1)}))
        return best

    def part2(self):
        self.visited = set()
        self.G = networkx.Graph()
        self.create_graph_of_interest(self.start_x, 0, (0, 0), 0)

        return self.get_best_path()

    def create_graph_of_interest(self, x, y, prev, length):
        if self.data[y][x] == "#":
            return
        open_neighbors = self.open_neighbors(x, y)
        if open_neighbors > 2 or x == self.end_x and y == len(self.data) - 1:
            self.G.add_edge(prev, (x, y), weight=length)
            prev = (x, y)
            length = 0

        if (x, y) in self.visited:
            return

        self.visited.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if 0 <= x + dx < len(self.data[0]) and 0 <= y + dy < len(self.data):
                self.create_graph_of_interest(x + dx, y + dy, prev, length + 1)

    def open_neighbors(self, x, y):
        count = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if 0 <= x + dx < len(self.data[0]) and 0 <= y + dy < len(self.data):
                if self.data[y + dy][x + dx] != "#":
                    count += 1
        return count

    def get_best_path(self):
        best = 0
        for path in networkx.all_simple_paths(
            self.G, (0, 0), (self.end_x, len(self.data) - 1)
        ):
            best = max(
                best,
                sum(
                    self.G[source][target]["weight"]
                    for source, target in zip(path, path[1:])
                ),
            )
        return best


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1},\t{'correct :)' if test1 == 94 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2},\t{'correct :)' if test2 == 154 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
