from collections import defaultdict
from pprint import pprint
import itertools
import re
import string
import sys
import os

sys.path.insert(0, "../../")
from utils.util import copy_answer, write_solution


class IntCodeComputer:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split(",")))

    def run_program(self, memory):
        for i in range(0, len(memory), 4):
            opcode = memory[i]
            try:
                if opcode == 99:
                    break
                elif opcode == 1:
                    self.opcode_1(memory, i)
                elif opcode == 2:
                    self.opcode_2(memory, i)
                else:
                    raise ValueError(f'Invalid opcode "{opcode}" at position {i}')
            except IndexError:
                return -1  # If we try to access an invalid memory address, return -1
        return memory[0]

    def opcode_1(self, memory, i):
        memory[memory[i + 3]] = memory[memory[i + 1]] + memory[memory[i + 2]]

    def opcode_2(self, memory, i):
        memory[memory[i + 3]] = memory[memory[i + 1]] * memory[memory[i + 2]]

    def part1(self):
        memory = self.data.copy()
        if not self.test:
            memory[1] = 12
            memory[2] = 2
        return self.run_program(memory)

    def part2(self):
        for noun, verb in itertools.product(range(100), range(100)):
            memory = self.data.copy()
            memory[1] = noun
            memory[2] = verb
            if self.run_program(memory) == 19690720:
                return 100 * noun + verb


def main():
    test = IntCodeComputer(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = IntCodeComputer()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)


if __name__ == "__main__":
    main()
