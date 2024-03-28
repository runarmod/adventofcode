import heapq
import itertools
import string
import time
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx


def _merge_edge(
    G: nx.Graph, remaining_node: tuple[int, int], remove_node: tuple[int, int]
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


def compactify(G: nx.Graph, removable: str = ".") -> None:
    """
    Removes all nodes with degree 2 that are in the string `removable`.

    Usefulness: If there is a long maze (1 wide) with optionally many dead-ends,
    this function will remove all the dead-ends and replace a long chain of 1 unit wide
    "corridors" with a single edge of the total length of the chain, from an intersection to another.
    """
    all_removable = set(removable.lower() + removable.upper())
    found = True
    while found:
        found = False
        for u in list(G.nodes):
            if 1 <= G.degree[u] <= 2 and G.nodes[u]["name"] in all_removable:
                v = list(G[u].keys())[0]
                _merge_edge(G, v, u)
                found = True


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().strip("\n").split("\n")
        self.endpoints = {}
        self.init_graph()
        self.connect_portals()
        compactify(self.G)
        # self.visualize()

    def init_graph(self):
        self.G = nx.Graph()
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                if c != ".":
                    continue
                self.G.add_node((x, y), name=c)
                for dx, dy in [(0, -1), (-1, 0)]:
                    if (x + dx, y + dy) in self.G:
                        self.G.add_edge((x, y), (x + dx, y + dy), weight=1)

    def _find_portal_node(self, data, pos1, pos2):
        for dx, dy in itertools.product(range(-1, 2), repeat=2):
            for x, y in [pos1, pos2]:
                if (
                    0 <= x + dx < len(data[0])
                    and 0 <= y + dy < len(data)
                    and data[y + dy][x + dx] == "."
                ):
                    return (x + dx, y + dy)

    def connect_portals(self):
        found = set()
        portals = defaultdict(set)
        for y, row in enumerate(self.data[:-1]):
            for x, c1 in enumerate(row[:-1]):
                if c1 not in string.ascii_uppercase:
                    continue
                if not any(
                    c2 in string.ascii_uppercase
                    for c2 in self.data[(y + 1)][x] + self.data[y][(x + 1)]
                ):
                    continue
                dx, dy = (
                    (1, 0) if self.data[y][x + 1] in string.ascii_uppercase else (0, 1)
                )
                word = c1 + self.data[y + dy][x + dx]
                if word not in found:
                    found.add(word)
                node = self._find_portal_node(self.data, (x, y), (x + dx, y + dy))
                if word in ["AA", "ZZ"]:
                    self.endpoints[word] = node
                portals[word[:2]].add(node)
                nx.set_node_attributes(self.G, {node: {"name": word}})

        for word, nodes in portals.items():
            if len(nodes) == 2:
                node1, node2 = nodes
                self.G.add_edge(node1, node2, weight=1)

    def visualize(self):
        pos = {(x, y): (x, -y) for (x, y) in self.G.nodes()}
        nx.draw(
            self.G, pos, with_labels=True, labels=nx.get_node_attributes(self.G, "name")
        )
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()

    def part1(self):
        return nx.shortest_path_length(
            self.G, self.endpoints["AA"], self.endpoints["ZZ"], weight="weight"
        )

    def is_outer(self, x, y):
        return x == 2 or x == len(self.data[0]) - 3 or y == 2 or y == len(self.data) - 3

    def part2(self):
        q = []
        heapq.heappush(q, (0, 0, self.endpoints["AA"], []))
        visited = set()

        while q:
            steps, level, node, path = heapq.heappop(q)
            if level == 0 and node == self.endpoints["ZZ"]:
                return steps
            if (node, level) in visited:
                continue
            visited.add((node, level))
            for n_x, n_y in self.G[node]:
                new_level = level
                if (
                    self.G[node][n_x, n_y]["weight"] == 1
                    and "."
                    != self.G.nodes[*node]["name"][:2]
                    == self.G.nodes[n_x, n_y]["name"][:2]
                ):
                    if not self.is_outer(*node) and self.is_outer(n_x, n_y):
                        new_level += 1
                    elif self.is_outer(*node) and not self.is_outer(n_x, n_y):
                        new_level -= 1
                new_steps = steps + self.G[node][n_x, n_y]["weight"]
                if new_level < 0:
                    continue
                heapq.heappush(
                    q, (new_steps, new_level, (n_x, n_y), path + [(n_x, n_y)])
                )
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 77 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 396 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
