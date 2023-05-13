import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()

    def generate_row(self, row):
        tmp = f".{row}."
        return "".join("^" if left != right else "." for left, right in zip(tmp, tmp[2:]))

    def generate_rows(self, start_row):
        row = start_row
        while True:
            row = self.generate_row(row)
            yield row

    def run(self, part):
        count = self.data.count(".")
        iterations = 10 if self.test else (40 if part == 1 else 400000)
        for row in itertools.islice(self.generate_rows(self.data), iterations - 1):
            count += row.count(".")
        return count

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    start = time.perf_counter()
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print()
    print(f"Time: {time.perf_counter() - start:.4f} sec")


if __name__ == "__main__":
    main()
