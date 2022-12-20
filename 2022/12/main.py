from collections import deque


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            line.strip() for line in open(filename).read().rstrip().split("\n")
        ]
        self.parse()

    def parse(self):
        self.q = deque()
        for j in range(len(self.data)):
            self.data[j] = list(self.data[j])
            for i in range(len(self.data[0])):
                if self.data[j][i] == "S":
                    self.start = (i, j)
                    self.data[j][i] = "a"
                elif self.data[j][i] == "E":
                    self.end = (i, j)
                    self.data[j][i] = "z"
                if self.data[j][i] == "a":
                    self.q.append((i, j, 0))
                self.data[j][i] = ord(self.data[j][i])

    def part1(self):
        return self.bfs()

    def part2(self):
        return self.bfs(self.q)

    def bfs(self, q=None):
        if q is None:
            q = deque()
            q.append((*self.start, 0))
        visited = {self.start}
        while q:
            x, y, steps = q.popleft()
            if (x, y) == self.end:
                return steps
            for x_c, y_c in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                if (
                    x + x_c < 0
                    or y + y_c < 0
                    or x + x_c >= len(self.data[0])
                    or y + y_c >= len(self.data)
                    or (x + x_c, y + y_c) in visited
                ):
                    continue

                if self.data[y + y_c][x + x_c] in range(self.data[y][x] + 2):
                    q.append((x + x_c, y + y_c, steps + 1))
                    visited.add((x + x_c, y + y_c))


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
