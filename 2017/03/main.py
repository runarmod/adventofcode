import itertools
import time
from typing import Generator


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = int(open(filename).read().rstrip())

    def get_coords(self) -> Generator[tuple[int, int], None, None]:
        x = y = 0
        length = 0

        yield x, y

        while True:
            for section in range(2):
                length += 1
                for side in range(2):
                    for _ in range(length):
                        match section * 2 + side:
                            case 0:
                                x += 1
                            case 1:
                                y += 1
                            case 2:
                                x -= 1
                            case 3:
                                y -= 1
                        yield x, y

    def part1(self):
        num = 1
        for x, y in self.get_coords():
            if num == self.data:
                return abs(x) + abs(y)
            num += 1

    def part2(self):
        d = {(0, 0): 1}

        for x, y in self.get_coords():
            d[x, y] = sum(
                d.get((x + dx, y + dy), 0)
                for dx, dy in itertools.product((-1, 0, 1), repeat=2)
            )

            if d[x, y] > self.data:
                return d[x, y]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 31 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 1968 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
