import functools
import os
import time


from Computer import Computer


def parseLines(lines):
    ip_index = int(lines[0].split(" ")[-1])

    return ip_index, [
        [opcode, int(a), int(b), int(c)]
        for opcode, a, b, c in [line.split(" ") for line in lines[1:]]
    ]


class Solution:
    def __init__(self):
        filename = "input.txt"
        self.ip_index, self.data = parseLines(open(filename).read().rstrip().split("\n"))
        self.number_part1 = 1017  # SEE stage6.asm
        self.number_part2 = 10551417  # SEE stage6.asm

    def old_part1(self):
        self.computer = Computer(self.data, self.ip_index)
        return self.computer.run()

    def old_part2(self):
        self.computer = Computer(self.data, self.ip_index)
        self.computer.set_register(0, 1)
        return self.computer.run()

    def sum_factors(self, n):
        # https://stackoverflow.com/a/6800214/10880273
        return sum(
            set(
                functools.reduce(
                    list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
                )
            )
        )

    def part1(self):
        return self.sum_factors(self.number_part1)

    def part2(self):
        return self.sum_factors(self.number_part2)


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
