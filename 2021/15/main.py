import itertools
from collections import defaultdict
from heapq import heappop, heappush


# COPY PASTE FROM https://gist.github.com/kachayev/5990802
def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    q, seen, mins = [(0, f, ())], set(), {f: 0}
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t:
                return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen:
                    continue
                prev = mins.get(v2, None)
                nxt = cost + c
                if prev is None or nxt < prev:
                    mins[v2] = nxt
                    heappush(q, (nxt, v2, path))

    return float("inf"), None


def generate_big_grid(data):
    out = []
    for y in range(5 * len(data)):
        l = []
        for x in range(5 * len(data)):
            if x < len(data) and y < len(data):
                l.append(data[y][x])
                continue
            if y < len(data):
                val = max(1, (l[x - len(data)] + 1) % 10)
                l.append(val)
            else:
                val = max(1, (out[y - len(data)][x] + 1) % 10)
                l.append(val)
        out.append(l)
    return out


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.small_grid = [
            list(map(int, line)) for line in open(filename).read().rstrip().split("\n")
        ]
        self.big_grid = generate_big_grid(self.small_grid)

    def create_edges(self, data):
        self.edges = []
        for y, x in itertools.product(range(len(data)), range(len(data))):
            for i, j in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < len(data) and 0 <= y + j < len(data):
                    self.edges.append(((x, y), (x + i, y + j), data[y + j][x + i]))

    def part1(self):
        data = self.small_grid
        self.create_edges(data)
        return dijkstra(self.edges, (0, 0), (len(data) - 1, len(data) - 1))[0]

    def part2(self):
        data = self.big_grid
        self.create_edges(data)
        return dijkstra(self.edges, (0, 0), (len(data) - 1, len(data) - 1))[0]


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")
    part2 = solution.part2()
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
