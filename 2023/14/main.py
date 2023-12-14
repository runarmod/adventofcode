import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [list(line) for line in open(filename).read().rstrip().split("\n")]

    def part1(self):
        self.tilt_north()
        return self.north_load()

    def north_load(self):
        return sum(
            len(self.data) - y
            for x, y in itertools.product(
                range(len(self.data[0])), range(len(self.data))
            )
            if self.data[y][x] == "O"
        )

    def tilt_north(self):
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if self.data[y][x] != "O":
                    continue
                ny = y - 1
                while ny >= 0 and self.data[ny][x] == ".":
                    ny -= 1
                self.data[ny + 1][x], self.data[y][x] = (
                    self.data[y][x],
                    self.data[ny + 1][x],
                )

    def tilt_east(self):
        for y in range(len(self.data)):
            for x in range(len(self.data[0]) - 1, -1, -1):
                if self.data[y][x] != "O":
                    continue
                nx = x + 1
                while nx < len(self.data[0]) and self.data[y][nx] == ".":
                    nx += 1
                self.data[y][nx - 1], self.data[y][x] = (
                    self.data[y][x],
                    self.data[y][nx - 1],
                )

    def tilt_south(self):
        for y in range(len(self.data) - 1, -1, -1):
            for x in range(len(self.data[0])):
                if self.data[y][x] != "O":
                    continue
                ny = y + 1
                while ny < len(self.data) and self.data[ny][x] == ".":
                    ny += 1
                self.data[ny - 1][x], self.data[y][x] = (
                    self.data[y][x],
                    self.data[ny - 1][x],
                )

    def tilt_west(self):
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if self.data[y][x] != "O":
                    continue
                nx = x - 1
                while nx >= 0 and self.data[y][nx] == ".":
                    nx -= 1
                self.data[y][nx + 1], self.data[y][x] = (
                    self.data[y][x],
                    self.data[y][nx + 1],
                )

    def get(self):
        return tuple("".join(line) for line in self.data)

    def cycle(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def part2(self):
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

        magic_number = 1000000000
        d = {}
        i = 1
        while i < magic_number:
            hashable = self.get()
            if hashable in d:
                dd = (magic_number - i) // (i - d[hashable]) * (i - d[hashable])
                if dd != 0:
                    i += dd
                    break
            d[hashable] = i
            self.cycle()
            i += 1

        while i < magic_number:
            self.cycle()
            i += 1

        return self.north_load()


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 136 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 64 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
