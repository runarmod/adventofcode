from collections import defaultdict


class Halt(Exception):
    pass


class Memory:
    def __init__(self, memory: list[int]):
        self.memory = defaultdict(int, enumerate(memory))

    def __getitem__(self, address: slice | int) -> list[int] | int:
        if isinstance(address, slice):
            return [
                self.memory[i]
                for i in range(address.start, address.stop, address.step or 1)
            ]
        return self.memory[address]

    def __setitem__(self, address, value):
        self.memory[address] = value

    def __repr__(self):
        return repr(self.memory)


class Address:
    def __init__(self, memory: Memory, address: int):
        self.memory = memory
        self.address = address
        self.location = self.memory[self.address]

    def refer_as_address(self):
        self.value = self.memory[self.location]

    def refer_as_value(self):
        self.value = self.location

    def refer_as_relative_base(self, base):
        self.location += base
        self.value = self.memory[self.location]

    def write(self, val):
        self.memory[self.location] = val


class IntcodeComputer:
    def __init__(self, nums, address):
        self.memory = Memory(nums[:])
        self.pc = 0
        self.halted = False
        self.latest_opcode = None
        self.idle = False
        self.operations = [
            lambda: None,
            self.add,
            self.mul,
            self.take_input,
            self.out,
            self.jt,
            self.jnt,
            self.lt,
            self.eq,
            self.adj_relative_base,
        ]
        self.arg_count = [0, 3, 3, 1, 1, 2, 2, 3, 3, 1]

        self.address = address
        self.inputs = [self.address]
        self.in_function = lambda: (self.inputs.pop(0) if self.inputs else -1)

        self.output = None
        # self.out_function = print
        self.outputs = []
        self.out_function = lambda o: self.outputs.append(o)

        self.relative_base: int = 0
        # self.run_until_io()

    def replace(self, index, value):
        self.memory[index] = value

    def push_input(self, *values: int):
        # self.inputs.append(value)
        for v in values:
            self.inputs.append(v)
        for _ in range(len(values)):
            self.run_until_io()

    def iter(self):
        while not self.halted:
            v = self.run()
            if v is None:
                break
            yield v

    def run_until_io(self):
        self.run(stop_on_output=True, stop_on_input=True)
        if self.stopped_on_input and not self.inputs:
            self.idle = True
        else:
            self.idle = False

    def get_all_outputs(self):
        while len(self.outputs) % 3 == 0 and self.outputs:
            yield self.get_three_outputs()

    def get_three_outputs(self):
        return self.outputs.pop(0), self.outputs.pop(0), self.outputs.pop(0)

    def run(self, stop_on_output=True, stop_on_input=False) -> int | None:
        self.halted = False
        self.output = None
        self.stopped_on_input = False
        self.latest_opcode = None
        while not self.halted:
            try:
                self.step()
            except Halt:
                self.halted = True
                break
            if stop_on_output and self.output is not None:
                break
            if self.latest_opcode == 3:
                self.stopped_on_input = True
                if stop_on_input:
                    break
        return self.output

    def step(self):
        opcode = self.memory[self.pc] % 100
        self.latest_opcode = opcode
        if opcode == 99:
            raise Halt

        assert opcode in range(1, len(self.operations)), opcode

        modes = [(self.memory[self.pc] // div) % 10 for div in [100, 1000, 10000]]
        parameters = [
            Address(self.memory, self.pc + 1 + i) for i in range(self.arg_count[opcode])
        ]

        for parameter, mode in zip(parameters, modes):
            [
                parameter.refer_as_address,
                parameter.refer_as_value,
                lambda: parameter.refer_as_relative_base(self.relative_base),
            ][mode]()

        self.pc += self.arg_count[opcode] + 1
        self.operations[opcode](*parameters)

    def add(self, a, b, c):
        c.write(a.value + b.value)

    def mul(self, a, b, c):
        c.write(a.value * b.value)

    def take_input(self, a):
        a.write(self.in_function())

    def out(self, a):
        self.output = a.value
        self.out_function(a.value)

    def jt(self, a, b):
        if a.value != 0:
            self.pc = b.value

    def jnt(self, a, b):
        if a.value == 0:
            self.pc = b.value

    def lt(self, a, b, c):
        c.write(int(a.value < b.value))

    def eq(self, a, b, c):
        c.write(int(a.value == b.value))

    def adj_relative_base(self, a):
        self.relative_base += a.value
