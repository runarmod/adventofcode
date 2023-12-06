import re
import time


def parseLine(line):
    return list(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        txt = open(filename).read().strip()
        self.time, self.distance = [parseLine(line) for line in txt.split("\n")]
        self.time2, self.distance2 = [
            parseLine(line) for line in txt.replace(" ", "").split("\n")
        ]

    def part1(self):
        mul = 1
        for time, distance in zip(self.time, self.distance):
            ways = 0
            for i in range(time):
                time_remaining = time - i
                distance_travelled = i * time_remaining
                if distance_travelled > distance:
                    ways += 1
            mul *= ways
        return mul

    def part2(self):
        time = self.time2[0]
        distance = self.distance2[0]

        ways = 0
        for i in range(time):
            time_remaining = time - i
            distance_travelled = i * time_remaining
            if distance_travelled > distance:
                ways += 1
        return ways


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
