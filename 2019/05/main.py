class Mode:
    POSITION, IMMEDIATE = range(2)


class IntCodeComputer:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split(",")))

    def run_program(self, memory):
        self.output = None
        i = 0
        while i < len(self.data):
            code = str(memory[i]).zfill(5)

            opcode = int(code[-2:])
            mode1 = Mode.POSITION if int(code[-3]) == 0 else Mode.IMMEDIATE
            mode2 = Mode.POSITION if int(code[-4]) == 0 else Mode.IMMEDIATE
            # mode3 = Mode.POSITION if int(code[-5]) == 0 else Mode.IMMEDIATE
            # print(f"{opcode=}, {mode1=}, {mode2=}, {mode3=}")
            try:
                match opcode:
                    case 99:
                        break
                    case 1:
                        i = self.opcode_1(memory, i, mode1, mode2)
                    case 2:
                        i = self.opcode_2(memory, i, mode1, mode2)
                    case 3:
                        i = self.opcode_3(memory, i)
                    case 4:
                        i = self.opcode_4(memory, i, mode1)
                    case 5:
                        i = self.opcode_5(memory, i, mode1, mode2)
                    case 6:
                        i = self.opcode_6(memory, i, mode1, mode2)
                    case 7:
                        i = self.opcode_7(memory, i, mode1, mode2)
                    case 8:
                        i = self.opcode_8(memory, i, mode1, mode2)
                    case _:
                        print(memory)
                        raise ValueError(f'Invalid opcode "{opcode}" at position {i}')
            except IndexError:
                return -1  # If we try to access an invalid memory address, return -1
            if self.output is not None:
                return self.output
        # pprint(memory)
        return memory[0]

    def opcode_1(self, memory, i, mode1, mode2):
        first = memory[memory[i + 1]] if mode1 == Mode.POSITION else memory[i + 1]
        second = memory[memory[i + 2]] if mode2 == Mode.POSITION else memory[i + 2]

        memory[memory[i + 3]] = first + second
        return i + 4

    def opcode_2(self, memory, i, mode1, mode2):
        first = memory[memory[i + 1]] if mode1 == Mode.POSITION else memory[i + 1]
        second = memory[memory[i + 2]] if mode2 == Mode.POSITION else memory[i + 2]

        memory[memory[i + 3]] = first * second
        return i + 4

    def opcode_3(self, memory, i):
        # val = int(input("Enter a value: "))
        memory[memory[i + 1]] = self.input
        return i + 2

    def opcode_4(self, memory, i, mode1):
        val = memory[memory[i + 1]] if mode1 == Mode.POSITION else memory[i + 1]
        if val != 0:
            self.output = val
            # print(f"Value: {val}")
        return i + 2

    def opcode_5(self, memory, i, mode1, mode2):
        val1 = memory[memory[i + 1]] if mode1 == Mode.POSITION else memory[i + 1]
        val2 = memory[memory[i + 2]] if mode2 == Mode.POSITION else memory[i + 2]
        return val2 if val1 != 0 else i + 3

    def opcode_6(self, memory, i, mode1, mode2):
        val1 = memory[memory[i + 1]] if mode1 == Mode.POSITION else memory[i + 1]
        val2 = memory[memory[i + 2]] if mode2 == Mode.POSITION else memory[i + 2]
        return val2 if val1 == 0 else i + 3

    def opcode_7(self, memory, i, mode1, mode2):
        val1 = memory[memory[i + 1]] if mode1 == Mode.POSITION else memory[i + 1]
        val2 = memory[memory[i + 2]] if mode2 == Mode.POSITION else memory[i + 2]

        memory[memory[i + 3]] = 1 if val1 < val2 else 0
        return i if memory[i + 3] == i else i + 4

    def opcode_8(self, memory, i, mode1, mode2):
        val1 = memory[memory[i + 1]] if mode1 == Mode.POSITION else memory[i + 1]
        val2 = memory[memory[i + 2]] if mode2 == Mode.POSITION else memory[i + 2]

        memory[memory[i + 3]] = 1 if val1 == val2 else 0
        return i if memory[i + 3] == i else i + 4

    def part1(self, input_val):
        self.input = input_val
        return self.run_program(self.data.copy())

    def part2(self, input_val):
        self.input = input_val
        return self.run_program(self.data.copy())


def main():
    test = IntCodeComputer(test=True)
    print(f"(TEST) Part 1: {test.part1(1)}")
    print(f"(TEST) Part 2: {test.part2(5)}")

    solution = IntCodeComputer()
    part1 = solution.part1(1)
    part2 = solution.part2(5)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
