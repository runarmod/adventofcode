import itertools
import time
from collections import deque
from typing import Generator


def parseData(
    data: list[str],
) -> tuple[set[tuple[int, int]], set[tuple[int, int]], tuple[int, int]]:
    locations = set()
    must_visit = set()
    loc_0 = (-1, -1)
    for y, x in itertools.product(range(len(data)), range(len(data[0]))):
        match data[y][x]:
            case "#":
                continue
            case ".":
                pass
            case "0":
                loc_0 = (x, y)
                must_visit.add((x, y))
            case _:
                must_visit.add((x, y))
        locations.add((x, y))
    return locations, must_visit, loc_0


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.locations, self.must_visit, self.coord_0 = parseData(
            open(filename).read().rstrip().split("\n")
        )

        self.distances = {}
        for start, end in itertools.combinations(self.must_visit, 2):
            self.distances[(start, end)] = self.distance(start, end)
            self.distances[(end, start)] = self.distances[(start, end)]

    def get_available_directions(self, x: int, y: int) -> Generator[tuple[int, int], None, None]:
        dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
        for dx, dy in dirs:
            if (x + dx, y + dy) in self.locations:
                yield x + dx, y + dy

    def distance(self, start: tuple[int, int], end: tuple[int, int]):
        seen: set[tuple[int, int]] = set()
        q: deque[tuple[set[int], tuple[int, int], int]] = deque([(set(), start, 0)])
        while q:
            visited, (x, y), steps = q.popleft()
            if (x, y) == end:
                return steps
            if (x, y) in seen:
                continue
            seen.add((x, y))
            for new_x, new_y in self.get_available_directions(x, y):
                q.append((visited.union(((new_x, new_y),)), (new_x, new_y), steps + 1))
        return None

    def dfs(self, start: tuple[int, int], remaining: set, part: int) -> int:
        if not remaining:
            # Either finished or have to go back to start
            return 0 if part == 1 else self.distances[(start, self.coord_0)]
        best = 999_999
        for coord in remaining:
            best = min(
                best,
                self.distances[(start, coord)]
                + self.dfs(coord, remaining.difference({coord}), part),
            )
        return best

    def part1(self):
        return self.dfs(self.coord_0, self.must_visit.difference({self.coord_0}), 1)

    def part2(self):
        return self.dfs(self.coord_0, self.must_visit.difference({self.coord_0}), 2)


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
