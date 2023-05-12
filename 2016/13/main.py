import functools
from collections import deque


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.magic_number = int(open(filename).read().rstrip())
        self.goal = (7, 4) if self.test else (31, 39)

    @functools.lru_cache(maxsize=0)
    def is_open(self, x, y):
        num = x * x + 3 * x + 2 * x * y + y + y * y
        num += self.magic_number
        return num.bit_count() % 2 == 0 and x >= 0 and y >= 0

    def bfs(self):
        visited = set()
        self.under50 = 0

        q = deque([((1, 1), 0)])
        while q:
            (x, y), steps = q.popleft()
            if (x, y) == self.goal:
                return steps
            if (x, y) in visited:
                continue
            visited.add((x, y))

            if steps <= 50:
                self.under50 += 1

            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                new_coords = (x + dx, y + dy)
                if not self.is_open(*new_coords):
                    continue
                q.append((new_coords, steps + 1))
        return -1

    def part1(self):
        return self.bfs()

    def part2(self):
        return self.under50


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
