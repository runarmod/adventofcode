import functools
import itertools
import re
import time
from collections import deque

from aoc_utils_runarmod import get_data


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_elems(data: list[str]):
    out = []
    for line in data:
        d = re.findall(r"(.) \|", line)
        if d:
            out.append(d)
    return out


keypad = get_elems(
    """
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
""".strip(
        "\n"
    ).splitlines()
)

navpad = get_elems(
    """
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
""".strip(
        "\n"
    ).splitlines()
)


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = get_data(2024, 21, test=test).strip("\n").split("\n")

        self.directions = {
            (0, -1): "^",
            (0, 1): "v",
            (-1, 0): "<",
            (1, 0): ">",
        }

    def get_paths(
        self, pad: list[list[str]], start: tuple[int, int], end: tuple[int, int]
    ):
        q = deque([[start]])

        while q:
            path = q.popleft()
            x, y = path[-1]
            if (x, y) == end:
                yield path
                continue
            for nx, ny in neighbors4((x, y)):
                if nx not in range(len(pad[0])) or ny not in range(len(pad)):
                    continue
                if (nx, ny) in path:
                    continue
                if pad[y][x] == " ":
                    continue
                q.append(path + [(nx, ny)])

    def path_as_moves(self, path: list[tuple[int, int]]):
        yield from (
            self.directions[b2[0] - b1[0], b2[1] - b1[1]]
            for b1, b2 in itertools.pairwise(path)
        )

    def coord(self, pad: list[list[str]], button: str) -> tuple[int, int]:
        return next(
            (
                (x, y)
                for x, y in itertools.product(range(len(pad[0])), range(len(pad)))
                if button == pad[y][x]
            )
        )

    def move_from_to(
        self, pad: list[list[str]], button1: str, button2: str, layer: int
    ) -> int:
        if button1 == button2:
            return 0

        coord1, coord2 = self.coord(pad, button1), self.coord(pad, button2)
        if layer == 0:
            return manhattan(coord1, coord2)

        return min(  # Use the path with the least moves
            sum(
                self.move_from_to_nav(b1, b2, layer - 1) + 1
                for b1, b2 in itertools.pairwise("A" + path)
            )  # Do all moves in path (starting from A)
            + self.move_from_to_nav(path[-1], "A", layer - 1)  # Reset to A
            for path in map(
                "".join,
                map(
                    self.path_as_moves,
                    self.get_paths(pad, coord1, coord2),
                ),
            )
        )

    @functools.cache
    def move_from_to_nav(self, a: str, b: str, layer: int) -> int:
        return self.move_from_to(navpad, a, b, layer)

    def run(self, robo_count: int) -> int:
        return sum(
            sum(
                self.move_from_to(keypad, k1, k2, robo_count) + 1
                for k1, k2 in itertools.pairwise("A" + line)  # Start on A
            )
            * nums(line)[0]
            for line in self.data
        )

    def part1(self):
        return self.run(2)

    def part2(self):
        return self.run(25)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 126384 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield point[:i] + (point[i] + diff,) + point[i + 1 :]


def manhattan(p1: tuple[int, ...], p2: tuple[int, ...]):
    return sum(abs(a - b) for a, b in zip(p1, p2))


if __name__ == "__main__":
    main()
