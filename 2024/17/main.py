import re
import time

import z3
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
        return ",".join(map(str, self.computer()))

    def computer(self):
        def combo(num):
            if num in range(4):
                return num
            if num in range(4, 7):
                return [self.A, self.B, self.C][num - 4]
            assert False, f"Invalid combo operand {num}"

        outputs = []
        pointer = 0
        while pointer in range(len(self.program)):
            match self.program[pointer]:
                case 0:
                    self.A = self.A >> combo(self.program[pointer + 1])
                case 1:
                    self.B = self.B ^ self.program[pointer + 1]
                case 2:
                    self.B = combo(self.program[pointer + 1]) % 8
                case 3:
                    if self.A != 0:
                        pointer = self.program[pointer + 1]
                        continue
                case 4:
                    self.B ^= self.C
                case 5:
                    outputs.append(combo(self.program[pointer + 1]) % 8)
                case 6:
                    self.B = self.A >> combo(self.program[pointer + 1])
                case 7:
                    self.C = self.A >> combo(self.program[pointer + 1])
            pointer += 2
        return outputs

    def part2(self):
        opt = z3.Optimize()
        s = z3.BitVec("s", 128)

        # TODO: Generalize this
        A, B, C = s, 0, 0
        for num in self.program:
            B = A % 8
            B = B ^ 3
            C = A >> B
            B = B ^ C
            A = A >> 3
            B = B ^ 5
            opt.add(B % 8 == num)

        opt.add(A == 0)
        opt.minimize(A)

        assert opt.check() == z3.sat
        answer = int(str(opt.model().eval(s)))  # How are we meant to convert to int?
        self.A = answer
        assert self.computer() == self.program
        return answer


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == '4,6,3,5,6,3,5,2,1,0' else 'wrong :('}"
    )
    # TODO: When having generalized part 2, test it
    # test2 = test.part2()
    # print(
    #     f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 117440 else 'wrong :('}"
    # )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
