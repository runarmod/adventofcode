import contextlib
from functools import lru_cache
import re


class Solution():
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.instructions = open(filename).read().rstrip().split("\n")
        self.data = {}
        self.generate_data()

    def generate_data(self):
        for instruction in self.instructions:
            cmd, key = instruction.split(" -> ")
            self.data[key] = cmd

    @lru_cache
    def get_value(self, wire):
        with contextlib.suppress(ValueError):
            return int(wire)

        cmd = self.data[wire].split(" ")

        if "NOT" in cmd:
            return ~self.get_value(cmd[1])
        elif "AND" in cmd:
            return self.get_value(cmd[0]) & self.get_value(cmd[2])
        elif "OR" in cmd:
            return self.get_value(cmd[0]) | self.get_value(cmd[2])
        elif "LSHIFT" in cmd:
            return self.get_value(cmd[0]) << self.get_value(cmd[2])
        elif "RSHIFT" in cmd:
            return self.get_value(cmd[0]) >> self.get_value(cmd[2])
        else:
            return self.get_value(cmd[0])

    def part1(self):
        return self.get_value("a")

    def part2(self):
        self.data["b"] = str(self.get_value("a"))
        self.get_value.cache_clear()
        return self.get_value("a")


def main():
    solution = Solution(test=False)
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")
    with open("solution.txt", "w") as f:
        f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
