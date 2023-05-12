from collections import defaultdict


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = [line.split(" ") for line in open(filename).read().rstrip().split("\n")]

    def old_run(self, part):
        registers = defaultdict(int)
        if part == 2:
            registers["c"] = 1

        def value(val):
            return registers[val] if val.isalpha() else int(val)

        i = 0
        while i < len(self.data):
            cmd, *options = self.data[i]
            match cmd:
                case "cpy":
                    registers[options[1]] = value(options[0])
                case "inc":
                    registers[options[0]] += 1
                case "dec":
                    registers[options[0]] -= 1
                case "jnz":
                    registers[options[1]] = value(options[0])
                    if value(options[0]) != 0:
                        i += int(options[1])
                        continue
                case _:
                    print("Should not be here...")
                    print(f"{cmd=}")
            i += 1

        return registers["a"]

    def optimized_run(self, part):
        a = 1
        b = 1
        c = 1 if part == 2 else 0

        # Generates fibonnaci numbers
        for _ in range(26 if c == 0 else 26 + 7):
            a, b = a + b, a

        return a + 17 * 18

    def part1(self):
        return self.optimized_run(1)

    def part2(self):
        return self.optimized_run(2)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
