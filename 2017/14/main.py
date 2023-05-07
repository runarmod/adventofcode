from hash import knothash


class Solution:
    def __init__(self, test: bool = False):
        filename = "testinput.txt" if test else "input.txt"
        self.word = open(filename).read().strip()

    def part1(self) -> int:
        count = 0
        self.grid: list[list[int]] = []
        for i in range(128):
            bitstring = "".join(bin(int(c, 16))[2:].zfill(4) for c in knothash(f"{self.word}-{i}"))
            self.grid.append(list(map(int, bitstring)))
            count += sum(map(int, bitstring))
        return count

    def collapse_region(self, x: int, y: int) -> None:
        if self.grid[y][x] == 0:
            return

        self.grid[y][x] = 0
        if x > 0:
            self.collapse_region(x - 1, y)
        if x < len(self.grid[y]) - 1:
            self.collapse_region(x + 1, y)
        if y > 0:
            self.collapse_region(x, y - 1)
        if y < len(self.grid) - 1:
            self.collapse_region(x, y + 1)

    def part2(self) -> int:
        count = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:
                    count += 1
                    self.collapse_region(x, y)
        return count


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
