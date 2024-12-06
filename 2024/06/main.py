import time

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        lines = (
            (get_data(2024, 6) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )

        self.pos = next(
            (x, y) for y, row in enumerate(lines) for x, c in enumerate(row) if c == "^"
        )

        self.pos = self.pos[0] + self.pos[1] * 1j
        self.dir = 0 + -1j  # up

        self.data = [list(line) for line in lines]
        self.seen = set()

    def value(self, pos):
        if 0 <= pos.imag < len(self.data) and 0 <= pos.real < len(self.data[0]):
            return self.data[int(pos.imag)][int(pos.real)]
        return None

    def part1(self):
        pos = self.pos
        self.seen.add(pos)
        direction = self.dir
        while 0 <= pos.imag < len(self.data) and 0 <= pos.real < len(self.data[0]):
            value = self.value(pos + direction)

            if value == "#":
                direction *= 1j
            elif value is None:
                break
            pos += direction
            self.seen.add(pos)

        return len(self.seen)

    def part2(self):
        s = 0

        for position in self.seen:
            x, y = int(position.real), int(position.imag)
            visited = set()
            pos = self.pos
            direction = self.dir

            if self.data[y][x] in "^#":
                continue
            self.data[y][x] = "#"

            while True:
                visited.add((pos, direction))
                value = self.value(pos + direction)
                if value == "#":
                    direction *= 1j
                elif value is None:
                    break
                else:
                    pos += direction
                if (pos, direction) in visited:
                    s += 1
                    break

            self.data[y][x] = "."

        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 41 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 6 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
