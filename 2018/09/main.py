import re
import time
from collections import defaultdict, deque


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.player_count, self.last_marble = tuple(
            map(int, re.findall(r"\d+", open(filename).read().rstrip()))
        )

    def run(self, last_marble):
        q = deque([0])
        players = defaultdict(int)

        for marble in range(1, last_marble + 1):
            if marble % 23 == 0:
                players[marble % self.player_count] += marble
                q.rotate(7)
                players[marble % self.player_count] += q.popleft()
            else:
                q.rotate(-2)
                q.appendleft(marble)

        return max(players.values())

    def part1(self):
        return self.run(self.last_marble)

    def part2(self):
        return self.run(self.last_marble * 100)


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
