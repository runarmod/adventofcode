import time
from collections import deque


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [list(line) for line in open(filename).read().rstrip().split("\n")]

    def part1(self):
        return self.get_energized_count((0, 0), 1 + 0j)

    def part2(self):
        best = 0
        for x in range(len(self.data[0])):
            for y in range(len(self.data)):
                if y == 0:
                    best = max(best, self.get_energized_count((x, y), 0 + 1j))
                if x == 0:
                    best = max(best, self.get_energized_count((x, y), 1 + 0j))
                if y == len(self.data) - 1:
                    best = max(best, self.get_energized_count((x, y), 0 - 1j))
                if x == len(self.data[0]) - 1:
                    best = max(best, self.get_energized_count((x, y), -1 + 0j))
        return best

    def get_energized_count(self, startPost: tuple[int, int], startDir: complex):
        states = set()
        visited = set()
        q = deque()
        q.append((*startPost, startDir))  # x, y, direction
        while q:
            x, y, d = q.popleft()
            if (x, y, d) in states:
                continue
            states.add((x, y, d))
            visited.add((x, y))

            new_directions: set[complex] = set()
            match self.data[y][x]:
                case ".":
                    new_directions.add(d)
                case "|":
                    if d.real == 0:
                        new_directions.add(d)
                    else:
                        new_directions.add(0 + 1j)
                        new_directions.add(0 - 1j)
                case "-":
                    if d.imag == 0:
                        new_directions.add(d)
                    else:
                        new_directions.add(1 + 0j)
                        new_directions.add(-1 + 0j)
                case "/":
                    if d.real == 0:
                        new_directions.add(d * 1j)
                    else:
                        new_directions.add(d * -1j)
                case "\\":
                    if d.real == 0:
                        new_directions.add(d * -1j)
                    else:
                        new_directions.add(d * 1j)
            for d in new_directions:
                if 0 <= x + int(d.real) < len(self.data[0]) and 0 <= y + int(
                    d.imag
                ) < len(self.data):
                    q.append((x + int(d.real), y + int(d.imag), d))
        return len(visited)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 46 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 51 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
