from collections import defaultdict
import re


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"

        instructionPattern = re.compile(r"(\w+) (.+)")
        self.instructions = [
            instructionPattern.match(i).groups()
            for i in open(filename).read().rstrip().split("\n")
        ]

    def run(self):
        conditionalJumpPattern = re.compile(r"(\w+), (\+?-?\d+)")
        i = 0
        while True:
            line = self.instructions[i]
            if line[0] == "hlf":
                self.registers[line[1]] //= 2
                i += 1
            elif line[0] == "tpl":
                self.registers[line[1]] *= 3
                i += 1
            elif line[0] == "inc":
                self.registers[line[1]] += 1
                i += 1
            elif line[0] == "jmp":
                i += int(line[1])
            elif line[0] == "jie":
                register, jmpAmout = conditionalJumpPattern.match(line[1]).groups()
                i += int(jmpAmout) if self.registers[register] % 2 == 0 else 1
            elif line[0] == "jio":
                register, jmpAmout = conditionalJumpPattern.match(line[1]).groups()
                i += int(jmpAmout) if self.registers[register] == 1 else 1
            else:
                raise ValueError(f"Invalid instruction: {line}")
            if i < 0 or i >= len(self.instructions):
                break
        return self.registers["a" if self.test else "b"]

    def part1(self):
        self.registers = defaultdict(int)
        return self.run()

    def part2(self):
        self.registers = defaultdict(int, a=1)
        return self.run()


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
