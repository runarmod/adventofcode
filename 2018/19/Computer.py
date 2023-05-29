from collections import Counter


class Computer:
    def __init__(self, program, ip_index):
        self.program = program
        self.op_functions = {
            "addr": lambda r, a, b, c: r[:c] + [r[a] + r[b]] + r[c + 1 :],
            "addi": lambda r, a, b, c: r[:c] + [r[a] + b] + r[c + 1 :],
            "mulr": lambda r, a, b, c: r[:c] + [r[a] * r[b]] + r[c + 1 :],
            "muli": lambda r, a, b, c: r[:c] + [r[a] * b] + r[c + 1 :],
            "banr": lambda r, a, b, c: r[:c] + [r[a] & r[b]] + r[c + 1 :],
            "bani": lambda r, a, b, c: r[:c] + [r[a] & b] + r[c + 1 :],
            "borr": lambda r, a, b, c: r[:c] + [r[a] | r[b]] + r[c + 1 :],
            "bori": lambda r, a, b, c: r[:c] + [r[a] | b] + r[c + 1 :],
            "setr": lambda r, a, _, c: r[:c] + [r[a]] + r[c + 1 :],
            "seti": lambda r, a, _, c: r[:c] + [a] + r[c + 1 :],
            "gtir": lambda r, a, b, c: r[:c] + [a > r[b]] + r[c + 1 :],
            "gtri": lambda r, a, b, c: r[:c] + [r[a] > b] + r[c + 1 :],
            "gtrr": lambda r, a, b, c: r[:c] + [r[a] > r[b]] + r[c + 1 :],
            "eqir": lambda r, a, b, c: r[:c] + [a == r[b]] + r[c + 1 :],
            "eqri": lambda r, a, b, c: r[:c] + [r[a] == b] + r[c + 1 :],
            "eqrr": lambda r, a, b, c: r[:c] + [r[a] == r[b]] + r[c + 1 :],
        }
        self.ip_index = ip_index
        self.registers = [0 for _ in range(6)]

    def set_register(self, index, value):
        self.registers[index] = value

    def run(self):
        counter = Counter()
        while 0 <= self.registers[self.ip_index] < len(self.program):
            counter[self.registers[self.ip_index]] += 1
            opcode, a, b, c = self.program[self.registers[self.ip_index]]

            self.registers = self.op_functions[opcode](self.registers, a, b, c)
            self.registers[self.ip_index] += 1

        return self.registers[0]
