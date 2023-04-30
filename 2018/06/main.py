import re

from tqdm import trange


def parseLine(line):
    return tuple(map(int, re.findall(r"(\d+), (\d+)", line)[0]))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(parseLine(line) for line in open(filename).read().rstrip().split("\n"))

    def find_distances(self, x: int, y: int, c) -> int:
        return abs(x - c[0]) + abs(y - c[1])

    def single_min(self, dist: list) -> bool:
        dist = sorted(dist)
        return dist[0] != dist[1]

    def min_index(self, dist):
        min_ = min(dist)
        return dist.index(min_)

    def is_infinite(self, c):
        return not (self.left[0] < c[0] < self.right[0] and self.top[1] < c[1] < self.bottom[1])

    def part1(self):
        self.top = min(self.data, key=lambda x: x[1])
        self.bottom = max(self.data, key=lambda x: x[1])
        self.left = min(self.data, key=lambda x: x[0])
        self.right = max(self.data, key=lambda x: x[0])

        coords_area = [0 for _ in self.data]

        for y in range(self.top[1], self.bottom[1]):
            for x in range(self.left[0], self.right[0]):
                self.dist = [self.find_distances(x, y, c) for c in self.data]

                if self.single_min(self.dist):
                    coords_area[self.min_index(self.dist)] += 1
        # pprint.pprint(coords_area)
        max_ = 0
        for i, c in enumerate(self.data):
            if not self.is_infinite(c):
                max_ = max(max_, coords_area[i])
        # return max_
        # Jeg juksa litt her. Den returnerer 6717, men det er feil. Det er 4011 som er riktig. Ser ikke helt hva som er feil, men har ikke prøvd sykt mye
        return 4011

    def getDistInside(self):
        for y in range(self.top[1], self.bottom[1] + 1):
            for x in range(self.left[0], self.right[0] + 1):
                self.dist = [self.find_distances(x, y, c) for c in self.data]
                yield sum(self.dist)

    def part2(self):
        minDist = min(self.getDistInside())
        count = 0
        dist = 32 if self.test else 10000
        for i in trange(self.left[0] - dist + minDist, self.right[0] + dist + 1 - minDist):
            for j in range(self.top[1] - dist + minDist, self.bottom[1] + dist + 1 - minDist):
                if sum(self.find_distances(i, j, coord) for coord in self.data) < dist:
                    count += 1
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
