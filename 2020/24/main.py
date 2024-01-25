import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.lines = open(filename).read().rstrip().split("\n")
        self.hexes = self.get_black_tiles()

    def get_black_tiles(self):
        hexes = set()

        for line in self.lines:
            x = y = 0
            i = 0
            while i < len(line):
                if line[i] == "e":
                    x += 1

                    i += 1
                elif line[i] == "w":
                    x -= 1

                    i += 1
                elif line[i : i + 2] == "ne":
                    y += 1

                    i += 2
                elif line[i : i + 2] == "nw":
                    x -= 1
                    y += 1

                    i += 2
                elif line[i : i + 2] == "sw":
                    y -= 1

                    i += 2
                elif line[i : i + 2] == "se":
                    x += 1
                    y -= 1

                    i += 2
            if (x, y) in hexes:
                hexes.remove((x, y))
            else:
                hexes.add((x, y))
        return hexes

    def part1(self):
        return len(self.hexes)

    def neighbours(self, hexagon: tuple[int, int]) -> set[tuple[int, int]]:
        return {
            (hexagon[0] + dx, hexagon[1] + dy)
            for dx, dy in ((0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1))
        }

    def remain_black(self, hexagon: tuple[int, int]) -> bool:
        return len(self.hexes & self.neighbours(hexagon)) in (1, 2)

    def part2(self):
        for _ in range(100):
            new_hexes = set()
            for hexagon in self.hexes:
                # Handle black tiles
                if self.remain_black(hexagon):
                    new_hexes.add(hexagon)

                # Handle white tiles (around black tiles)
                for neighbour in self.neighbours(hexagon):
                    if neighbour in self.hexes:
                        # Neighbour is black
                        continue
                    # Neighbour is white
                    if len(self.hexes & self.neighbours(neighbour)) == 2:
                        new_hexes.add(neighbour)
            self.hexes = new_hexes
        return len(self.hexes)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 10 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 2208 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
