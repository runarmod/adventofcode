import re
import time
from collections import defaultdict, namedtuple


op_functions = {
    "addr": lambda r, a, b, c: r[:c] + [r[a] + r[b]]    + r[c + 1 :],
    "addi": lambda r, a, b, c: r[:c] + [r[a] + b]       + r[c + 1 :],
    "mulr": lambda r, a, b, c: r[:c] + [r[a] * r[b]]    + r[c + 1 :],
    "muli": lambda r, a, b, c: r[:c] + [r[a] * b]       + r[c + 1 :],
    "banr": lambda r, a, b, c: r[:c] + [r[a] & r[b]]    + r[c + 1 :],
    "bani": lambda r, a, b, c: r[:c] + [r[a] & b]       + r[c + 1 :],
    "borr": lambda r, a, b, c: r[:c] + [r[a] | r[b]]    + r[c + 1 :],
    "bori": lambda r, a, b, c: r[:c] + [r[a] | b]       + r[c + 1 :],
    "setr": lambda r, a, _, c: r[:c] + [r[a]]           + r[c + 1 :],
    "seti": lambda r, a, _, c: r[:c] + [a]              + r[c + 1 :],
    "gtir": lambda r, a, b, c: r[:c] + [a > r[b]]       + r[c + 1 :],
    "gtri": lambda r, a, b, c: r[:c] + [r[a] > b]       + r[c + 1 :],
    "gtrr": lambda r, a, b, c: r[:c] + [r[a] > r[b]]    + r[c + 1 :],
    "eqir": lambda r, a, b, c: r[:c] + [a == r[b]]      + r[c + 1 :],
    "eqri": lambda r, a, b, c: r[:c] + [r[a] == b]      + r[c + 1 :],
    "eqrr": lambda r, a, b, c: r[:c] + [r[a] == r[b]]   + r[c + 1 :],
}


def parse_first_part(lines):
    Section = namedtuple("Section", ["before", "instruction", "after"])
    return Section(*[[int(x) for x in re.findall(r"\d+", line)] for line in lines])


def get_possible_opcodes(before, instruction, after):
    registers = before[:]
    return [
        func_name
        for func_name in op_functions
        if op_functions[func_name](registers, *instruction[1:]) == after
    ]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        first_half, self.program = open(filename).read().rstrip().split("\n" * 4)

        self.sections = [
            parse_first_part(section.split("\n")) for section in first_half.split("\n\n")
        ]

    def part1(self):
        return sum(len(get_possible_opcodes(*section)) >= 3 for section in self.sections)

    def part2(self):
        possible_opcodes = defaultdict(set)
        for section in self.sections:
            for opcode in get_possible_opcodes(*section):
                possible_opcodes[section.instruction[0]].add(opcode)

        opcode_map = {}
        while len(opcode_map) < 16:
            for opcode, possible in possible_opcodes.items():
                if len(possible) == 1:
                    opcode_map[opcode] = possible.pop()
                    for other in possible_opcodes.values():
                        other.discard(opcode_map[opcode])
                    break

        registers = [0, 0, 0, 0]
        for line in self.program.split("\n"):
            opcode, a, b, c = [int(x) for x in re.findall(r"\d+", line)]
            registers = op_functions[opcode_map[opcode]](registers, a, b, c)

        return registers[0]


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
