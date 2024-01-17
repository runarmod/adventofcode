from collections import Counter
import functools
from textwrap import dedent
import numpy as np
import time


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
        self.possible_edges = set(self.get_edges())

    def get_edges(self):
        for _ in range(2):
            for _ in range(4):
                yield "".join(self.tile[0])
                self.rotate()
            self.flip()

    def rotate(self):
        self.tile = np.rot90(self.tile)

    def flip(self):
        self.tile = np.flip(self.tile, 0)

    def rotate_until_top(self, top: str):
        for _ in range(2):
            for _ in range(4):
                if "".join(self.tile[0]) == top:
                    return True
                self.rotate()
            self.flip()
        return False

    def rotate_until_left(self, left: str):
        for _ in range(2):
            for _ in range(4):
                if "".join(line[0] for line in self.tile) == left:
                    return True
                self.rotate()
            self.flip()
        return False

    def rotate_until_right_and_bottom(self, right: str, bottom: str):
        for _ in range(2):
            for _ in range(4):
                if (
                    "".join(self.tile[-1]) == bottom
                    and "".join(line[-1] for line in self.tile) == right
                ):
                    return True
                self.rotate()
            self.flip()
        return False

    def get_right_side(self):
        return "".join(line[-1] for line in self.tile)

    def get_bottom_side(self):
        return "".join(self.tile[-1])

    def get_common_side(self, other):
        for side in self.possible_edges:
            if side in other.possible_edges:
                return side


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

        self.monster = (
            dedent(
                """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
            )
            .strip("\n")
            .split("\n")
        )

        self.monster_coords = {
            (x, y)
            for y, line in enumerate(self.monster)
            for x, char in enumerate(line)
            if char == "#"
        }

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

    def orient_top_left(self, top_left):
        id_top_left_neighbours = list(self.neighbours[top_left.ID])

        top_left_neighbour_right = self.tiles_by_id[id_top_left_neighbours[0]]
        common_right = top_left.get_common_side(top_left_neighbour_right)

        top_left_neighbour_bottom = self.tiles_by_id[id_top_left_neighbours[1]]
        common_bottom = top_left.get_common_side(top_left_neighbour_bottom)

        for right, bottom in zip(
            (common_right, common_right[::-1], common_right, common_right[::-1]),
            (common_bottom, common_bottom, common_bottom[::-1], common_bottom[::-1]),
        ):
            if top_left.rotate_until_right_and_bottom(right, bottom):
                break

    def fill_image(self, image):
        for y in range(len(image)):
            for x in range(len(image[0])):
                if x == 0 and y == 0:
                    continue
                if x == 0:
                    side_to_get = image[y - 1][x].get_bottom_side()
                    for tile_id in self.neighbours[image[y - 1][x].ID]:
                        tile = self.tiles_by_id[tile_id]
                        if tile.rotate_until_top(side_to_get):
                            image[y][x] = tile
                            break
                    else:
                        assert False
                else:
                    side_to_get = image[y][x - 1].get_right_side()
                    for tile_id in self.neighbours[image[y][x - 1].ID]:
                        tile = self.tiles_by_id[tile_id]
                        if tile.rotate_until_left(side_to_get):
                            image[y][x] = tile
                            break
                    else:
                        assert False

    def find_monsters(self, image) -> bool:
        """
        THIS MODIFIES THE IMAGE
        """
        real_monster_coords = set()
        for y in range(len(image) - len(self.monster)):
            for x in range(len(image[0]) - len(self.monster[0])):
                if all(image[y + dy][x + dx] in "#O" for dx, dy in self.monster_coords):
                    real_monster_coords |= {
                        (x + dx, y + dy) for dx, dy in self.monster_coords
                    }

                    for dx, dy in self.monster_coords:
                        image[y + dy][x + dx] = "O"
        return len(real_monster_coords)

    def part2(self):
        image = np.array(
            [
                [None for _ in range(round(len(self.neighbours) ** 0.5))]
                for _ in range(round(len(self.neighbours) ** 0.5))
            ]
        )

        # Choose random corner tile as top-left
        top_left = next(
            tile for tile in self.tiles if len(self.neighbours[tile.ID]) == 2
        )
        image[0][0] = top_left

        self.orient_top_left(top_left)
        self.fill_image(image)

        concatinated = np.block(
            [[tile.tile[1:-1, 1:-1] for tile in line] for line in image]
        )

        for _ in range(2):
            for _ in range(4):
                if self.find_monsters(concatinated):
                    return Counter(concatinated.flatten())["#"]
                concatinated = np.rot90(concatinated)
            concatinated = np.flip(concatinated, 0)

        assert False


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1},\t{'correct :)' if test1 == 20899048083289 else 'wrong :('}"
    )
    test2 = test.part2()
    print(f"(TEST) Part 2: {test2},\t\t{'correct :)' if test2 == 273 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
