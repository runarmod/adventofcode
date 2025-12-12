import time

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        *shapes, regions = get_data(2025, 12, test=test).strip("\n").split("\n\n")
        shapes = [shape.split("\n")[1:] for shape in shapes]
        self.regions = [region.split(": ") for region in regions.split("\n")]
        self.shape_content_sizes = [
            sum(row.count("#") for row in shape) for shape in shapes
        ]
        shape_bound_sizes = {(len(shape[0]), len(shape)) for shape in shapes}
        if len(shape_bound_sizes) == 1:
            self.shape_w, self.shape_h = shape_bound_sizes.pop()
        else:
            self.shape_w, self.shape_h = (
                max(x for x, y in shape_bound_sizes),
                max(y for x, y in shape_bound_sizes),
            )

    def part1(self):
        lower_bound = upper_bound = 0
        for dimension, counts in self.regions:
            w, h = map(int, dimension.split("x"))
            counts = tuple(map(int, counts.split(" ")))
            upper_bound += w * h >= sum(
                count * size for count, size in zip(counts, self.shape_content_sizes)
            )

            count = sum(counts)
            fit_w = w // self.shape_w
            fit_h = h // self.shape_h
            lower_bound += fit_w * fit_h >= count

        if lower_bound == upper_bound:
            return lower_bound

        return f"Answer is in range [{lower_bound}, {upper_bound}]"


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 2 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
