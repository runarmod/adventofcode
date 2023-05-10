import itertools


def get_before_after_grids(line):
    before, after = tuple(
        tuple(tuple(map(lambda x: 1 if x == "#" else 0, list(c))) for c in l.split("/"))
        for l in line.split(" => ")
    )

    def get_all_rotations(before):
        returned = set()
        for _ in range(4):
            if (before := tuple(zip(*before[::-1]))) not in returned:
                returned.add(before)
                yield before
            if (mirrored := tuple(row[::-1] for row in before)) not in returned:
                returned.add(mirrored)
                yield mirrored

    for inn in get_all_rotations(before):
        yield inn, after


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = {
            before: after
            for line in open(filename).read().rstrip().split("\n")
            for before, after in get_before_after_grids(line)
        }
        start_grid = ".#./..#/###"
        self.grid = tuple(tuple(int(c == "#") for c in line) for line in start_grid.split("/"))

    def get_new_grid(self, grid_size):
        new_grid = []
        for row in range(0, len(self.grid), grid_size):
            new_squares = []
            for col in range(0, len(self.grid), grid_size):
                grid = [self.grid[row + r][col : col + grid_size] for r in range(grid_size)]
                new_squares.append(self.data[tuple(tuple(x) for x in grid)])
            for rowIdx in range(len(new_squares[0])):
                new_row = [square[rowIdx] for square in new_squares]
                new_grid.append(tuple(itertools.chain(*new_row)))
        return tuple(new_grid)

    def run(self, iterations):
        for _ in range(iterations):
            square_dim = 2 if len(self.grid) % 2 == 0 else 3
            self.grid = self.get_new_grid(square_dim)

    def lights_on(self):
        return sum(sum(row) for row in self.grid)

    def part1(self):
        self.run(2 if self.test else 5)
        return self.lights_on()

    def part2(self):
        if self.test:
            return "N/A"
        self.run(18 - 5)
        return self.lights_on()


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
