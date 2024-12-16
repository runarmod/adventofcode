import heapq
import itertools
import time

from aoc_utils_runarmod import get_data


def parseGrid(lines: list[str]):
    return [list(line) for line in lines]


class Solution:
    def __init__(self, test: bool = False):
        self.test = test
        data = (
            (get_data(2024, 16) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )

        self.data = parseGrid(data)

        for y, line in enumerate(self.data):
            for x, c in enumerate(line):
                if c == "S":
                    self.start = (x, y)
                    self.data[y][x] = "."
                if c == "E":
                    self.end = (x, y)
                    self.data[y][x] = "."

        self.visited_forward, self.record = self.navigate(
            self.start, [(1, 0)], self.end, 1
        )
        self.visited_backward, _ = self.navigate(
            self.end, [(1, 0), (0, -1)], self.start, -1
        )

    def navigate(
        self,
        start_pos: tuple[int, int],
        start_dirs: list[tuple[int, int]],
        goal: tuple[int, int],
        step: int,
    ):
        visited: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}

        q: list[tuple[int, tuple[int, int], tuple[int, int], list[tuple[int, int]]]] = (
            []
        )
        for start_dir in start_dirs:
            heapq.heappush(q, (0, start_pos, start_dir, [start_pos]))

        record: int | None = None

        while q:
            points, position, direction, path = heapq.heappop(q)
            if (position, direction) in visited:
                continue
            visited[(position, direction)] = points

            if position == goal and record is None:
                record = points

            direction_c = complex(*direction)
            for new_direction in [direction_c * 1j, direction_c * -1j]:
                heapq.heappush(
                    q,
                    (
                        points + 1000,
                        position,
                        (round(new_direction.real), round(new_direction.imag)),
                        path[:],
                    ),
                )
            new_position = (
                position[0] + direction[0] * step,
                position[1] + direction[1] * step,
            )
            if self.data[new_position[1]][new_position[0]] == ".":
                heapq.heappush(
                    q,
                    (points + 1, new_position, direction, path + [new_position]),
                )

        return visited, record

    def part1(self):
        return self.record

    def part2(self):
        positions: set[tuple[int, int]] = set()
        for x, y, direction in itertools.product(
            range(len(self.data[0])),
            range(len(self.data)),
            [(1, 0), (0, 1), (-1, 0), (0, -1)],
        ):
            if ((x, y), direction) not in self.visited_forward or (
                (x, y),
                direction,
            ) not in self.visited_backward:
                continue

            if (
                self.visited_forward[((x, y), direction)]
                + self.visited_backward[((x, y), direction)]
                == self.record
            ):
                positions.add((x, y))

        return len(positions)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 11048 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 64 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
