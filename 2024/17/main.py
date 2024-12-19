import re
import time

from aoc_utils_runarmod import get_data


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            get_data(2024, 17) if not self.test else open("testinput.txt").read()
        ).rstrip()

        self.A, self.B, self.C, *self.program = self.data = parseNumbers(data)

    def part1(self):
        return ",".join(map(str, self.run_computer()))

    def part2(self):
        return self.find_A()

    def get_next_output(self, A, B, C, pointer=0):
        def combo(num):
            if num in range(4):
                return num
            if num in range(4, 7):
                return [A, B, C][num - 4]
            assert False, f"Invalid combo operand {num}"

        while pointer in range(len(self.program)):
            operand = self.program[pointer + 1]
            match self.program[pointer]:
                case 0:
                    A >>= combo(operand)
                case 1:
                    B ^= operand
                case 2:
                    B = combo(operand) >> 3
                case 3:
                    if A != 0:
                        pointer = operand
                        continue
                case 4:
                    B ^= C
                case 5:
                    return combo(operand) % 8, A, B, C, pointer + 2
                case 6:
                    B = A >> combo(operand)
                case 7:
                    C = A >> combo(operand)
            pointer += 2

    def run_computer(self):
        pointer = 0
        outs = []
        A, B, C = self.A, self.B, self.C
        while pointer in range(len(self.program)):
            ret = self.get_next_output(A, B, C, pointer)
            if ret is None:
                break
            out, A, B, C, pointer = ret
            outs.append(out)
        return outs

    def find_A(self, A: int = 0, program_index: int = None):
        if program_index is None:
            program_index = len(self.program) - 1
        elif program_index < 0:
            return A

        for tmp_A in range(2**3):
            new_A = A << 3 | tmp_A
            res, *_ = self.get_next_output(new_A, 0, 0, 0)
            if res != self.program[program_index]:
                continue
            try:
                out = self.find_A(new_A, program_index - 1)
                return out
            except ValueError as _:
                continue
        # Backtrack
        raise ValueError("This value of A does not work")


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1}, {'correct :)' if test1 == '5,7,3,0' else 'wrong :('}"
    )
    test2 = test.part2()
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 117440 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
