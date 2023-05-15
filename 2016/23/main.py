from collections import defaultdict
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "modified_input.txt"
        self.data = [line.split(" ") for line in open(filename).read().rstrip().split("\n")]

    def run(self, part):
        registers = defaultdict(int)

        if not self.test:
            registers["a"] = 7
        if part == 2:
            registers["a"] = 12

        def value(val):
            return registers[val] if val.isalpha() else int(val)

        data = [row[:] for row in self.data]

        i = 0
        while i < len(data):
            cmd, *options = data[i]

            match cmd:
                case "cpy":
                    registers[options[1]] = value(options[0])
                case "inc":
                    registers[options[0]] += 1
                case "dec":
                    registers[options[0]] -= 1
                case "jnz":
                    if value(options[0]) != 0:
                        i += value(options[1])
                        continue
                case "tgl":
                    distance = value(options[0])
                    if 0 <= i + distance < len(data):
                        if data[i + distance][0] == "inc":
                            change = "dec"
                        elif len(data[i + distance]) == 2:
                            change = "inc"
                        elif data[i + distance][0] == "jnz":
                            change = "cpy"
                        else:
                            change = "jnz"
                        data[i + distance][0] = change
                case "nop":
                    # Self made: skips line
                    # Is added to make sure total lines/line placement is kept
                    # And makes sure jnz jumps to correct line
                    # Same as "jnz 0 0" or "cpy a a"
                    pass
                case "mul":
                    # Self made:
                    # "mul x y" sets x to x * y
                    # basically same as the following, but MUUUUCH FASTER
                    # cpy b c
                    # inc a
                    # dec c
                    # jnz c -2
                    # dec d
                    # jnz d -5
                    # ^ This translates to a+=b*d; b=0; c=0
                    registers[options[0]] *= value(options[1])
                case _:
                    print("Should not be here...")
                    print(f"{cmd=}")
            i += 1

        return registers["a"]

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)


def main():
    start = time.perf_counter()
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
