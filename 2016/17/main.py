import hashlib
from collections import deque


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.passcode = open(filename).read().rstrip()
        self.bfs()

    def hash(self, string):
        return hashlib.md5(string.encode()).hexdigest()

    def get_directions(self, x, y, last_steps):
        _hash = self.hash(self.passcode + last_steps)
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))  # up, down, left, right
        for i in range(4):
            if _hash[i] in {"b", "c", "d", "e", "f"}:
                new_x, new_y = x + directions[i][0], y + directions[i][1]
                if 0 <= new_x < 4 and 0 <= new_y < 4:
                    yield *directions[i], "UDLR"[i]

    def bfs(self):
        self.answer1 = None
        self.answer2 = 0

        visited = set()  # (x, y, steps)
        q = deque([(0, 0, "")])  # (x, y, steps)
        while q:
            x, y, steps = q.popleft()

            if (x, y) == (3, 3):
                if self.answer1 is None:
                    self.answer1 = steps
                self.answer2 = max(self.answer2, len(steps))
                continue

            if (x, y, steps) in visited:
                continue

            visited.add((x, y, steps))
            for dx, dy, dir_letter in self.get_directions(x, y, steps):
                q.append((x + dx, y + dy, steps + dir_letter))
        return None

    def part1(self):
        return self.answer1

    def part2(self):
        return self.answer2


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
