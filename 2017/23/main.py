import math
from collections import defaultdict


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [line.split(" ") for line in open(filename).read().rstrip().split("\n")]

    def part1(self):
        registers = defaultdict(int)

        def val(value):
            return registers[value] if value.isalpha() else int(value)

        used = 0
        i = 0
        while i < len(self.data):
            cmd, *args = self.data[i][:]
            if len(args) == 2:
                a, b = args
            else:
                a = args[0]

            match cmd:
                case "set":
                    registers[a] = val(b)
                case "sub":
                    registers[a] -= val(b)
                case "mul":
                    registers[a] *= val(b)
                    used += 1
                case "jnz":
                    if val(a) != 0:
                        i += val(b) - 1
            i += 1
        return used

    def part2(self):
        def is_prime(n):
            return all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

        return sum(not is_prime(b) for b in range(107900, 124900 + 1, 17))


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
