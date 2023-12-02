import re
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        data = [
            re.findall(r"(\d+) (\w+)", line)
            for line in open(filename).read().rstrip().split("\n")
        ]
        self.max_per_line = [
            {
                color: max(int(pair[0]) for pair in line if pair[1] == color)
                for color in ("green", "red", "blue")
            }
            for line in data
        ]

    def part1(self):
        return sum(
            game_nr
            for game_nr, game in enumerate(self.max_per_line, start=1)
            if not (game["red"] > 12 or game["green"] > 13 or game["blue"] > 14)
        )

    def part2(self):
        return sum(
            game["red"] * game["green"] * game["blue"] for game in self.max_per_line
        )


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
