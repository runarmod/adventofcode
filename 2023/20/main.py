from collections import deque
from math import lcm
import itertools
import re
import time


def parseLine(line):
    f, l = line.split(" -> ")
    return f[0] if f[0] in "&%" else "", re.findall(r"\w+", f)[0], l.split(", ")


class Module:
    def __init__(self, type, name, children):
        self.type = type
        self.name = name
        self.children = children
        self.state = False

        self.memory = {}

    def flip(self, state, sender):
        if self.type == "":
            return self.children[:], False, self.name
        if self.type == "%":
            if state:
                return [], False, self.name
            self.state = not self.state
            return self.children[:], self.state, self.name
        elif self.type == "&":
            self.memory[sender] = state
            return self.children[:], not all(self.memory.values()), self.name
        assert False


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.lines = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]
        self.modules = {}
        for type, name, children in self.lines:
            self.modules[name] = Module(type, name, children)

        for name, module in self.modules.items():
            for child in module.children:
                if child in self.modules:
                    self.modules[child].memory[name] = False

    def part1(self):
        return self.solve(1)

    def part2(self):
        return self.solve(2)

    def solve(self, part):
        q = deque()  # (module_name, signal_high, sender)
        lows = highs = 0
        interest = {
            k: None
            for k in self.modules[
                next(
                    filter(
                        lambda node: "rx" in node.children,
                        [m for m in self.modules.values()],
                    )
                ).name
            ].memory.keys()
        }

        cycles = {}
        for i in itertools.count():
            q.append(("broadcaster", False, "button"))
            while q:
                reciever, state, sender = q.popleft()
                if i < 1000:
                    if state:
                        highs += 1
                    else:
                        lows += 1
                elif part == 1:
                    return lows * highs

                if reciever in interest and state == False:
                    if interest[reciever] is not None:
                        cycles[reciever] = i - interest[reciever]
                        del interest[reciever]
                        if not interest and part == 2:
                            return lcm(*cycles.values())
                    else:
                        interest[reciever] = i

                # if module_name == "rx" and not high:  # PLEASE ._.
                #     return i

                if reciever in self.modules.keys():
                    module = self.modules[reciever]
                    new_recievers, state, new_sender = module.flip(state, sender)
                    for reciever in new_recievers:
                        q.append((reciever, state, new_sender))
        assert False


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()

    print(
        f"(TEST) Part 1: {test1},\t{'correct :)' if test1 == 32000000 else 'wrong :('}"
    )

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
