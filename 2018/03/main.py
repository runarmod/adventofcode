import re
import numpy as np

def parseLine(line, pattern):
    match = list(map(int, re.match(pattern, line).groups()))
    return match


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        pattern = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
        self.data = [parseLine(line, pattern) for line in open(filename).read().rstrip().split("\n")]

        

    def part1(self):
        grid  = np.zeros((1000, 1000))
        for claim in self.data:
            grid[claim[1]:claim[1]+claim[3], claim[2]:claim[2]+claim[4]] += 1
        count = 0
        for row in grid:
            for col in row:
                if col > 1:
                    count += 1
        return count

    def part2(self):
        res = []
        grid  = np.zeros((1000, 1000))
        for claim in self.data:
            for y in range(claim[1], claim[1]+claim[3]):
                for x in range(claim[2], claim[2]+claim[4]):
                    if grid[y][x] != -1 and grid[y][x] != 0:
                        grid[y][x] = -1
                    else:
                        grid[y][x] = claim[0]
        for claim in self.data:
            valid = True
            for y in range(claim[1], claim[1]+claim[3]):
                for x in range(claim[2], claim[2]+claim[4]):
                    if grid[y][x] == -1:
                        valid = False
                        break
            if valid:
                res.append(claim[0])
        return res


def main():
    solution = Solution(test=False)
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
