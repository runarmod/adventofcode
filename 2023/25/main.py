import functools
import matplotlib.pyplot as plt
import networkx as nx
import operator
import re
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            re.split(r"(?:: )| ", line)
            for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        # A more elegant way: nx.minimum_edge_cut
        self.G = nx.Graph()
        for node, *nodes in self.data:
            for node2 in nodes:
                self.G.add_edge(node, node2)

        # Uncomment next to lines to see the minimum cut
        # nx.draw(self.G, with_labels=True)
        # plt.show()

        # Seen from the graph above (edit as needed)
        if self.test:
            self.G.remove_edge("pzl", "hfx")
            self.G.remove_edge("nvd", "jqt")
            self.G.remove_edge("cmg", "bvb")
        else:
            self.G.remove_edge("zcj", "rtt")
            self.G.remove_edge("txl", "hxq")
            self.G.remove_edge("gxv", "tpn")

        return functools.reduce(
            operator.mul, (len(g) for g in nx.connected_components(self.G)), 1
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 54 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
