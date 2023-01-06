class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            line.split(")") for line in open(filename).read().rstrip().split("\n")
        ]

    def create_graph(self):
        self.graph = {}
        for center, orbit in self.data:
            self.graph[orbit] = center

    def part1(self):
        self.create_graph()
        ### Counts all distances from all nodes to COM
        s = 0
        for orbit, center in self.graph.items():
            if orbit in ("YOU", "SAN"):
                continue
            if center == "COM":
                s += 1
                continue
            node = orbit
            while node != "COM":
                s += 1
                node = self.graph[node]
        return s

    def create_parents_list(self, node):
        if node == "COM":
            return ["COM"]
        l = self.create_parents_list(self.graph[node])
        if not l:
            return [node]
        return [node] + l

    def part2(self):
        parents_YOU = self.create_parents_list("YOU")
        parents_SAN = self.create_parents_list("SAN")
        first_common = next((i for i in parents_SAN if i in parents_YOU), None)
        
        # Minus 2 because it's from santa's parent to YOU's parent, not from santa to YOU
        return parents_YOU.index(first_common) + parents_SAN.index(first_common) - 2


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
