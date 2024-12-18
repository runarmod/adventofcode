import re
import time

import networkx as nx
from aoc_utils_runarmod import get_data


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 18) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )

        self.data = list(map(parseNumbers, data))
        self.W, self.H = (71, 71) if not self.test else (7, 7)
        self.G = self.create_graph(12 if self.test else 1024)

    def create_graph(self, fallen_bytes_count: int):
        corrupted = {coord for coord in self.data[:fallen_bytes_count]}
        free = {(x, y) for x in range(self.W) for y in range(self.H)} - corrupted
        G = nx.Graph()
        for coord in free:
            for neighbor in neighbors4(coord):
                if neighbor in free:
                    G.add_edge(coord, neighbor)
        return G

    def part1(self):
        return nx.shortest_path_length(self.G, (0, 0), (self.W - 1, self.H - 1))

    def part2(self):
        for i in range(self.W * self.H - self.G.number_of_nodes() + 1, len(self.data)):
            prev_node = self.data[i - 1]
            self.G.remove_node(prev_node)
            if not nx.has_path(self.G, (0, 0), (self.W - 1, self.H - 1)):
                return ",".join(map(str, prev_node))
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 22 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == '6,1' else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield point[:i] + (point[i] + diff,) + point[i + 1 :]


if __name__ == "__main__":
    main()
