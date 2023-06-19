import time
from collections import deque
import networkx as nx


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()[1:-1]
        self.G = self.generate_graph()
        self.shortest_paths: dict[complex, int] = nx.shortest_path_length(self.G, 0)

    def generate_graph(self):
        states: deque[tuple[set[complex], set[complex]]] = deque()
        cur_positions: set[complex] = {0 + 0j}
        starts: set[complex] = {0}
        ends: set[complex] = set()
        directions: dict[str, complex] = {"N": 1j, "S": -1j, "E": 1, "W": -1}

        G = nx.Graph()
        for c in self.data:
            if c == "(":
                states.append((starts, ends))
                starts, ends = cur_positions, set()
            elif c == ")":
                cur_positions |= ends
                starts, ends = states.pop()
            elif c == "|":
                ends |= cur_positions
                cur_positions = starts
            elif c in "NSEW":
                G.add_edges_from((p, p + directions[c]) for p in cur_positions)
                cur_positions = {p + directions[c] for p in cur_positions}
        return G

    def part1(self):
        return max(self.shortest_paths.values())

    def part2(self):
        return sum(length >= 1000 for length in self.shortest_paths.values())


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
