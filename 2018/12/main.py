import time
from collections import defaultdict


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"

        first_line, last_lines = open(filename).read().rstrip().split("\n\n")
        self.map = first_line.split(" ")[-1]

        self.conversions = defaultdict(lambda: ".")
        for line in last_lines.split("\n"):
            frm, to = line.split(" => ")
            self.conversions[frm] = to

    def grid_iteration(self, grid, start_index):
        grid = f".....{grid}....."
        new_grid = "".join(
            self.conversions["".join(sub)]
            for sub in zip(grid, grid[1:], grid[2:], grid[3:], grid[4:])
        )
        new_grid = new_grid.rstrip(".")

        return (
            new_grid.strip("."),
            3 - new_grid.index("#") + start_index,
        )  # Add the padding minus the removed empty start plants

    def part1(self):
        return self.run(20)

    def part2(self):
        return self.run(50_000_000_000)

    def run(self, generations):
        grid = self.map
        start_index = 0

        seen = {}
        round_nr = 0
        skipped = False

        while round_nr < generations:
            round_nr += 1
            grid, start_index = self.grid_iteration(grid, start_index)
            if grid in seen and not skipped:
                cycle_length = round_nr - seen[grid][0]
                iterations = (generations - round_nr) // cycle_length
                round_nr += iterations * cycle_length
                start_index += iterations * (start_index - seen[grid][1])
                skipped = True
            seen[grid] = (round_nr, start_index)
        return sum(i - start_index for i in range(len(grid)) if grid[i] == "#")


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
