import itertools
import time


def parseData(lines):
    d = [[None for _ in range(len(lines[0]))] for _ in range(len(lines))]
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            match lines[y][x]:
                case ".":
                    continue
                case ">":
                    d[y][x] = (1, 0)
                case "v":
                    d[y][x] = (0, 1)
    return d


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = parseData(open(filename).read().rstrip().split("\n"))

    def move(self, state: list[list[tuple[int, int] | None]], turn: tuple[int, int]):
        new_state: list[list[tuple[int, int] | None]] = [
            [None for _ in range(len(state[0]))] for _ in range(len(state))
        ]

        moved = False

        for y in range(len(state)):
            for x in range(len(state[0])):
                if state[y][x] is None:
                    continue

                dx, dy = state[y][x]
                if (dx, dy) != turn:
                    new_state[y][x] = (dx, dy)
                    continue

                nx, ny = (x + dx) % len(state[0]), (y + dy) % len(state)

                if state[ny][nx] is not None:
                    new_state[y][x] = (dx, dy)
                    continue

                moved = True
                new_state[ny][nx] = state[y][x]

        return new_state, moved

    def part1(self):
        state = self.data
        for round in itertools.count(start=1):
            state, moved1 = self.move(state, (1, 0))
            state, moved2 = self.move(state, (0, 1))
            if not (moved1 or moved2):
                return round


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 58 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
