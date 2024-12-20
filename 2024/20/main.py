import time
from collections import deque

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 20) if not self.test else open("testinput.txt").read())
            .strip("\n")
            .split("\n")
        )
        self.grid = data

        self.walls = set()
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                if c == "S":
                    self.start = x, y
                elif c == "E":
                    self.end = x, y
                elif c == "#":
                    self.walls.add((x, y))

        self.from_start = self.bfs_out(self.start)
        self.to_end = self.bfs_out(self.end)

    def bfs_out(self, start_pos) -> dict[tuple[int, int], int]:
        distances = {}
        q = deque()
        q.append((start_pos, 0))
        while q:
            pos, dist = q.popleft()
            if pos in distances:
                continue

            if pos[0] not in range(len(self.grid[0])) or pos[1] not in range(
                len(self.grid)
            ):
                continue

            distances[pos] = dist
            if start_pos == self.start and pos == self.end:
                self.no_cheat_distance = dist

            for neighbor in neighbors4(pos):
                if neighbor not in self.walls:
                    q.append((neighbor, dist + 1))
        return distances

    def find_route_count(self, max_jump_dist: int):
        valid = 0
        for pos1, dist1 in self.from_start.items():
            for pos2 in get_close_points(pos1, max_jump_dist):
                dist2 = self.to_end.get(pos2, None)
                if dist2 is None:
                    continue
                jump_dist = manhattan(pos1, pos2)
                total_dist = dist1 + dist2 + jump_dist
                if total_dist <= self.no_cheat_distance - (50 if self.test else 100):
                    valid += 1
        return valid

    def part1(self):
        return self.find_route_count(2)

    def part2(self):
        return self.find_route_count(20)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 1 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 285 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


def get_close_points(point: tuple[int, int], max_distance: int):
    x, y = point
    yield x, y
    for distance in range(max_distance + 1):
        for offset in range(distance):
            invOffset = distance - offset
            yield x + offset, y + invOffset
            yield x + invOffset, y - offset
            yield x - offset, y - invOffset
            yield x - invOffset, y + offset


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield point[:i] + (point[i] + diff,) + point[i + 1 :]


def manhattan(p1: tuple[int, ...], p2: tuple[int, ...]):
    return sum(abs(a - b) for a, b in zip(p1, p2))


if __name__ == "__main__":
    main()
