import itertools
import re


def parseLine(line):
    return tuple(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = tuple(map(parseLine, open(filename).read().rstrip().split("\n")))

    def run(self, data):
        return next(
            (
                i
                for i in itertools.count()
                if all(
                    (pos0 + i + disc_nr) % positions == 0 for disc_nr, positions, _, pos0 in data
                )
            ),
            -1,
        )

    def part1(self):
        return self.run(self.data)

    def part2(self):
        new_disc = parseLine("Disc #7 has 11 positions; at time=0, it is at position 0.")
        data = list(self.data)
        data.append(new_disc)
        return self.run(data)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
