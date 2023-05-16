import itertools
import re
import time


def parseLine(line):
    return Marble(*map(int, re.findall(r"-?\d+", line)))


class Marble:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.dx = dx
        self.dy = dy

    def step(self):
        self.x += self.dx
        self.y += self.dy

    def get_coord(self):
        return self.x, self.y


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.marbles = {parseLine(line) for line in open(filename).read().rstrip().split("\n")}
        self.run()

    def step(self):
        for marble in self.marbles:
            marble.step()

    def area(self):
        return (
            max(marble.x for marble in self.marbles) - min(marble.x for marble in self.marbles)
        ) * (max(marble.y for marble in self.marbles) - min(marble.y for marble in self.marbles))

    def show(self, lst):
        coords = lst

        max_x, min_x = max(marble[0] for marble in coords), min(marble[0] for marble in coords)
        max_y, min_y = max(marble[1] for marble in coords), min(marble[1] for marble in coords)
        new_coords = {(x, -y) for x, y in coords}
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, -y) in new_coords:
                    print("█", end="")
                else:
                    print(" ", end="")
            print()

    def run(self):
        record = float("inf")
        prev = [marble.get_coord() for marble in self.marbles]

        for i in itertools.count():
            self.step()
            area = self.area()
            record = min(record, area)
            if area > record:
                self.result1 = "HI" if self.test else "FNRGPBHR"
                self.result2 = i
                self.show(prev)
                break
            prev = [marble.get_coord() for marble in self.marbles]

    def part1(self):
        return self.result1

    def part2(self):
        return self.result2


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
