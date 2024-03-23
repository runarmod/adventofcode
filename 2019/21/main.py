import time

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))

    def part1(self):
        # !(A && B && C) && D
        program = ("OR A J", "AND B J", "AND C J", "NOT J J", "AND D J", "WALK")
        return self.run_program(program)

    def part2(self):
        # !(A && B && C) && D && (E || H)
        program = (
            "OR A J",
            "AND B J",
            "AND C J",
            "NOT J J",
            "AND D J",
            "OR E T",
            "OR H T",
            "AND T J",
            "RUN",
        )
        return self.run_program(program)

    def run_program(self, program):
        computer = IntcodeComputer(self.data)
        computer.inputs = list(map(ord, "\n".join(program) + "\n"))
        for output_char in computer.iter():
            try:
                # print(chr(output_char), end="")
                chr(output_char)
            except ValueError:
                return int(output_char)
        return None


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
