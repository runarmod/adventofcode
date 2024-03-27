import string
import time
from typing import Generator

import networkx as nx


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")

    def initialize_graph(self):
        self.G = nx.Graph()
        self.letters = {}

        for y, line in enumerate(self.data):
            for x, c in enumerate(line):
                if c == "#":
                    continue
                self.G.add_node((x, y), name=c)
                if c == "@":
                    self.start = (x, y)
                elif c in string.ascii_lowercase:
                    self.letters[c] = (x, y)
                for dx, dy in [(0, 1), (1, 0)]:
                    n_x, n_y = x + dx, y + dy
                    if (
                        0 <= n_x < len(line)
                        and 0 <= n_y < len(self.data)
                        and self.data[n_y][n_x] != "#"
                    ):
                        self.G.add_edge((x, y), (n_x, n_y), weight=1)
        self.compactify(self.G)

    def _merge_edge(
        self, G: nx.Graph, remaining_node: tuple[int, int], remove_node: tuple[int, int]
    ):
        """
        Merges the edge between `remaining_node` and `remove_node` into a single edge.

        The weight of the new edge is the sum of the weights of the two edges.
        """
        remove_weight = G.edges[remaining_node, remove_node]["weight"]
        edit_edges = list(G.edges(remove_node, data=True))
        for u, v, data in edit_edges:
            if remaining_node in [u, v]:
                continue
            G.remove_edge(u, v)
            if u == remove_node:
                G.add_edge(remaining_node, v, weight=data["weight"] + remove_weight)
            elif v == remove_node:
                G.add_edge(remaining_node, u, weight=data["weight"] + remove_weight)
            else:
                assert False
        G.remove_node(remove_node)

    def compactify(self, G: nx.Graph, removable: str = ".") -> None:
        """
        Removes all nodes with degree 2 that are in the string `removable`.

        Usefulness: If there is a long maze (1 wide) with optionally many deadends,
        this function will remove all the deadends and replace a long chain of 1 unit long
        edges with a single edge of the total length of the chain, from an intersection to another.
        """
        all_removable = set(removable.lower() + removable.upper())
        found = True
        while found:
            found = False
            for u in list(G.nodes):
                if G.degree[u] <= 2 and G.nodes[u]["name"] in all_removable:
                    v = list(G[u].keys())[0]
                    self._merge_edge(G, v, u)
                    found = True

    def possible_moves(
        self, G: nx.Graph, start: tuple[int, int], remaining_keys: set[str]
    ) -> Generator[tuple[str, tuple[int, int], int], None, None]:
        done = set(self.letters) - remaining_keys
        legal = ".@" + "".join(done) + "".join(done).upper()
        for letter in remaining_keys:
            coord = self.letters[letter]
            try:
                for path in nx.all_shortest_paths(G, start, coord):
                    if not all(
                        G.nodes[path[i]]["name"] in legal
                        for i in range(1, len(path) - 1)
                    ):
                        continue
                    length = sum(
                        G.edges[path[i], path[i + 1]]["weight"]
                        for i in range(len(path) - 1)
                    )
                    yield letter, path[-1], length
                    break
            except nx.NetworkXNoPath:
                pass

    def distance_to_collect_keys(self, G, start, remaining_keys):
        if len(remaining_keys) == 0:
            return 0
        froz = frozenset(remaining_keys)
        if (start, froz) in self.cache:
            return self.cache[start, froz]

        res = float("inf")
        for letter, end, length in self.possible_moves(G, start, remaining_keys):
            res = min(
                res,
                length
                + self.distance_to_collect_keys(G, end, remaining_keys - {letter}),
            )
        self.cache[start, froz] = res
        return res

    def part1(self):
        self.initialize_graph()
        self.cache = {}
        return self.distance_to_collect_keys(
            self.G, self.start, set(self.letters.keys())
        )

    def modify_data_around_start(self):
        """
        Modifies the data around the start to look like this:\n
        ```c
        @#@
        ###
        @#@
        ```
        """
        x, y = self.start
        self.data[y - 1] = self.data[y - 1][: x - 1] + "@#@" + self.data[y - 1][x + 2 :]
        self.data[y] = self.data[y][: x - 1] + "###" + self.data[y][x + 2 :]
        self.data[y + 1] = self.data[y + 1][: x - 1] + "@#@" + self.data[y + 1][x + 2 :]

    def keys_in_graph(self, G: nx.Graph) -> set[str]:
        """
        Returns the set of keys in the graph.
        AKA lowercase letters. (Uppercase letters are doors)
        """
        return set(
            G.nodes[u]["name"]
            for u in G.nodes
            if G.nodes[u]["name"] in string.ascii_lowercase
        )

    def part2(self):
        self.modify_data_around_start()
        self.initialize_graph()

        best = 0
        for G in (self.G.subgraph(c).copy() for c in nx.connected_components(self.G)):
            self.cache = {}
            keys = self.keys_in_graph(G)
            self.compactify(G, "." + "".join(set(string.ascii_lowercase) - keys))
            start = next(node for node in G.nodes if G.nodes[node]["name"] == "@")
            best += self.distance_to_collect_keys(G, start, keys)
        return best


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 50 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 24 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
