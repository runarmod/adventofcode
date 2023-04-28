import functools
import itertools
import re


def parseLine(line):
    return tuple((1 if "on" in line else 0, *map(int, re.findall(r"(-?\d+)", line))))


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]
        self.part1data = [line for line in self.data if all(abs(x) <= 50 for x in line[1:])]

    def part1(self):
        return self.run(self.part1data)

    def part2(self):
        return self.run(self.data)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def intersection(s, t):
        function = [lambda _, b: -b, max, min, max, min, max, min]
        new_cuboid = tuple(function[i](s[i], t[i]) for i in range(7))
        return (
            None
            if new_cuboid[1] > new_cuboid[2]  # Doesn't intersect on x axis
            or new_cuboid[3] > new_cuboid[4]  # Doesn't intersect on y axis
            or new_cuboid[5] > new_cuboid[6]  # Doesn't intersect on z axis
            else new_cuboid
        )

    def run(self, data):
        cores = []
        for cube in data:
            # Only add the current cuboid if it is on
            toadd = [cube] if cube[0] == 1 else []

            # Add the intersection of the current cuboid with all previous cuboids
            # If an intersection should be removed, it will start with -1
            for core in cores:
                if inter := Solution.intersection(cube, core):
                    toadd += [inter]
            cores += toadd
        # Sum volume of all the cuboids (subtract the volume of the removed cuboids (c[0]))
        return sum(c[0] * (c[2] - c[1] + 1) * (c[4] - c[3] + 1) * (c[6] - c[5] + 1) for c in cores)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")
    part2 = solution.part2()
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
