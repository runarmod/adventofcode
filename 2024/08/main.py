import itertools
import time
from collections import defaultdict

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = (
            (get_data(2024, 8) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )

        self.WIDTH = len(self.data[0])
        self.HEIGHT = len(self.data)

        self.positions = defaultdict(list)
        for y, row in enumerate(self.data):
            for x, val in enumerate(row):
                if val != ".":
                    self.positions[val].append((x, y))

    def get_antenna_combinations(self):
        for positions in self.positions.values():
            for pos1, pos2 in itertools.combinations(positions, 2):
                yield sorted([pos1, pos2])

    def get_diff(self, pos1, pos2):
        return pos2[0] - pos1[0], pos2[1] - pos1[1]

    def get_antinode_inside_count(self, antinodes):
        return sum(
            0 <= antinode[0] < self.WIDTH and 0 <= antinode[1] < self.HEIGHT
            for antinode in antinodes
        )

    def part1(self):
        antinodes = set()
        for pos1, pos2 in self.get_antenna_combinations():
            diff = self.get_diff(pos1, pos2)
            antinodes.add((pos1[0] - diff[0], pos1[1] - diff[1]))
            antinodes.add((pos2[0] + diff[0], pos2[1] + diff[1]))
        return self.get_antinode_inside_count(antinodes)

    def get_diagonal_antinodes(self, pos, diff, direction):
        offset = 0
        while (
            0 <= pos[0] + diff[0] * offset < self.WIDTH
            and 0 <= pos[1] + diff[1] * offset < self.HEIGHT
        ):
            yield (pos[0] + diff[0] * offset, pos[1] + diff[1] * offset)
            offset += direction

    def part2(self):
        antinodes = set()
        for pos1, pos2 in self.get_antenna_combinations():
            diff = self.get_diff(pos1, pos2)
            antinodes.update(self.get_diagonal_antinodes(pos1, diff, -1))
            antinodes.update(self.get_diagonal_antinodes(pos2, diff, 1))
        return self.get_antinode_inside_count(antinodes)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 14 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 34 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
