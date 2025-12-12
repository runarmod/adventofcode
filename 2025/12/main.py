import time

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        *shapes, regions = get_data(2025, 12, test=test).strip("\n").split("\n\n")
        shapes = [shape.split("\n")[1:] for shape in shapes]
        self.regions = [region.split(": ") for region in regions.split("\n")]
        self.shapes_sizes = [sum(row.count("#") for row in shape) for shape in shapes]

    def part1(self):
        s = 0
        for dimension, counts in self.regions:
            x, y = map(int, dimension.split("x"))
            counts = map(int, counts.split(" "))
            s += x * y >= sum(
                count * size for count, size in zip(counts, self.shapes_sizes)
            )
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 3 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
