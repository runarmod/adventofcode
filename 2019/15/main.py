import itertools
import time
from enum import Enum

import networkx as nx

from IntcodeComputer import IntcodeComputer


class Type(Enum):
    WALL, CLEAR, TANK, UNKNOWN = range(4)


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))
        self.walkable = nx.Graph()
        self.all_visible = nx.Graph()
        self.run()

    def run(self):
        coord = 0 + 0j
        grid: dict[complex, Type] = {}
        for d in (1, 1j, -1, -1j):
            grid[coord + d] = Type.UNKNOWN

        dir_to_imag = {1: 0 + 1j, 2: 0 - 1j, 3: -1 + 0j, 4: 1 + 0j}
        imag_to_dir = {v: k for k, v in dir_to_imag.items()}

        self.tank = None
        self.all_visible.add_edges_from(
            [(0 + 0j, 0 + 1j), (0 + 0j, 0 - 1j), (0 + 0j, -1 + 0j), (0 + 0j, 1 + 0j)]
        )

        ds = []

        computer = IntcodeComputer(self.data)
        while not computer.halted and Type.UNKNOWN in grid.values():
            if not ds:
                shortest = nx.shortest_path(
                    self.all_visible,
                    coord,
                    next(c for c, t in grid.items() if t == Type.UNKNOWN),
                )
                for c1, c2 in itertools.pairwise(shortest):
                    ds.append(imag_to_dir[c2 - c1])

            d = ds.pop(0)
            computer.input(d)

            answer = computer.run()
            if answer is None:
                print("Answer is None")
                quit()

            ty = Type(answer)
            new_coord = coord + dir_to_imag[d]
            grid[new_coord] = ty
            if ty == Type.TANK:
                self.tank = new_coord

            if ty == Type.WALL:
                continue
            self.walkable.add_edge(coord, new_coord)
            coord = new_coord
            for nd in (1, 1j, -1, -1j):
                if coord + nd not in grid:
                    grid[coord + nd] = Type.UNKNOWN
                    self.all_visible.add_edge(coord, coord + nd)

    def part1(self):
        return nx.shortest_path_length(self.all_visible, 0 + 0j, self.tank)

    def part2(self):
        return max(
            nx.single_source_shortest_path_length(self.walkable, self.tank).values()
        )


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
