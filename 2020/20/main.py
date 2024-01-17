import functools
import numpy as np
import os
import sys
import time

sys.path.insert(0, "../../")
from utils import copy_answer, request_submit, write_solution


def parseTile(lines):
    header = lines[0]
    tile_id = int(header.split(" ")[-1][:-1])
    tile = [list(line) for line in lines[1:]]
    return tile_id, tile


class Tile:
    def __init__(self, tile_id, tile):
        self.ID = tile_id
        self.tile = np.array(tile)
        self.neighbors: list[Tile] = []
        self.possible_edges = self.get_edges()

    def get_edges(self):
        edges = set()
        for _ in range(2):
            for _ in range(4):
                edges.add("".join(self.tile[0]))
                self.rotate()
            self.flip()
        return edges

    def rotate(self):
        self.tile = np.rot90(self.tile)

    def flip(self):
        self.tile = np.flip(self.tile, 0)

    def __repr__(self):
        return f"{self.ID}"


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseTile(lines.split("\n"))
            for lines in open(filename).read().rstrip().split("\n\n")
        ]

        self.tiles = {Tile(tile_id, tile) for tile_id, tile in self.data}
        self.neighbours = {
            tile_nr: (
                {
                    tile_nr2
                    for tile_nr2, tile2 in (
                        (tmp_tile.ID, tmp_tile.possible_edges)
                        for tmp_tile in self.tiles
                    )
                    if len(tile & tile2)
                }
                - {tile_nr}
            )
            for tile_nr, tile in (
                (tmp_tile.ID, tmp_tile.possible_edges) for tmp_tile in self.tiles
            )
        }

        self.tiles_by_id = {tile.ID: tile for tile in self.tiles}

    def part1(self):
        return functools.reduce(
            lambda a, b: a * b,
            (
                tile_nr
                for tile_nr, neighbours in self.neighbours.items()
                if len(neighbours) == 2
            ),
            1,
        )

    def part2(self):
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 20899048083289 else 'wrong :('}"
    )
    test2 = test.part2()
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == None else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit(2020, 20, part1, part2)


if __name__ == "__main__":
    main()
