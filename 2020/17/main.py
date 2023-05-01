from collections import defaultdict
from itertools import product


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.state = {
            (colNr, rowNr)
            for rowNr, line in enumerate(open(filename).read().rstrip().split("\n"))
            for colNr, char in enumerate(line)
            if char == "#"
        }

    def get_neighbours(self, higherdims):
        for deltaDims in product((-1, 0, 1), repeat=len(higherdims)):
            if any(d != 0 for d in deltaDims):
                yield tuple(hi + di for hi, di in zip(higherdims, deltaDims))

    def run_iteration(self, state):
        neighbours = defaultdict(int)
        for pos in state:
            for neighbour in self.get_neighbours(pos):
                neighbours[neighbour] += 1

        return {
            neighbour
            for neighbour, count in neighbours.items()
            if neighbour in state and count == 2 or count == 3
        }

    def convert_to_dimensions(self, state, dimensions):
        return {(c[0], c[1], *(0 for _ in range(dimensions - 2))) for c in state}

    def part1(self):
        return self.run(3)

    def part2(self):
        return self.run(4)

    def run(self, dimensions):
        state = self.convert_to_dimensions(self.state, dimensions)
        for _ in range(6):
            state = self.run_iteration(state)
        return len(state)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")
    part2 = solution.part2()
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
