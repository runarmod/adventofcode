import itertools
import random
import time
from collections import deque
from copy import deepcopy

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(2024, 24, test=test).strip("\n").split("\n\n")

        self.first = data[0].split("\n")
        self.last = list(map(lambda x: x.split(" -> "), data[1].split("\n")))
        self.wires = {}
        for line in self.first:
            wire, val = line.split(": ")
            self.wires[wire] = int(val)

        self.gates = {v: k for k, v in self.last}
        self.max_z = max(
            map(lambda x: int(x[1:]), filter(lambda x: x.startswith("z"), self.gates))
        )

    def calculate(self, x: int, y: int, gates: dict[str, str]) -> int:
        wires = {}
        assert x.bit_length() <= self.max_z, f"{x.bit_length()=}"
        assert y.bit_length() <= self.max_z, f"{y.bit_length()=}"
        for i in range(self.max_z):
            wires[f"x{i:02}"] = (x >> i) & 1
            wires[f"y{i:02}"] = (y >> i) & 1

        return sum(self.eval(f"z{i:02}", wires, gates) << i for i in range(self.max_z))

    def eval(self, wire, wires=None, gates=None):
        if gates is None:
            gates = self.gates
        if wires is None:
            wires = self.wires

        if wire in wires:
            return wires[wire]
        a, op, b = gates[wire].split()
        a_val = self.eval(a, wires, gates)
        b_val = self.eval(b, wires, gates)
        match op:
            case "AND":
                v = a_val & b_val
            case "OR":
                v = a_val | b_val
            case "XOR":
                v = a_val ^ b_val
        wires[wire] = v
        return v

    def part1(self):
        return sum(self.eval(f"z{i:02}") << i for i in range(self.max_z + 1))

    def first_mistake(self, gates: dict[str, str]) -> int:
        first = float("inf")
        for _ in range(self.max_z):  # TODO: find a better way to find the first mistake
            # (There is no logic in looping exactly self.max_z times,
            #  other than as we have larger numbers, we should try more numbers)
            x, y = random.getrandbits(self.max_z), random.getrandbits(self.max_z)
            xy = x + y
            z = self.calculate(x, y, gates)
            if z == xy:
                continue
            # https://stackoverflow.com/a/40354822/10880273
            pos = ((xy ^ z) & (-(xy ^ z))).bit_length() - 1
            if pos != -1 and pos < first:
                first = pos
        return first

    def get_ancestors(
        self,
        wire: str,
        gates: dict[str, str],
        include_self: bool = True,
        include_inputs: bool = False,
    ):
        if include_self:
            yield wire
        if wire[0] in "xy":
            return
        a, _, b = gates[wire].split()
        q = deque([a, b])
        while q:
            node = q.popleft()
            if not include_inputs and node[0] in "xy":
                continue
            yield node
            if node[0] not in "xy":
                a, _, b = gates[node].split()
                q.extend([a, b])

    def find_swap_pair(self):
        worst_z_v = self.first_mistake(self.gates)
        for swap1, swap2 in itertools.product(
            self.get_ancestors(f"z{worst_z_v:02}", self.gates), self.gates
        ):
            if swap1 == swap2:
                continue
            gates = deepcopy(self.gates)
            gates[swap1], gates[swap2] = gates[swap2], gates[swap1]
            try:
                new_worst = self.first_mistake(gates)
            except RecursionError:
                continue
            if new_worst <= worst_z_v:  # Bad swap
                continue
            return swap1, swap2
        else:
            assert False, "No swaps found. Try again."

    def part2(self):
        swaps = []
        for _ in range(4):
            swap1, swap2 = self.find_swap_pair()
            swaps.extend((swap1, swap2))
            self.gates[swap1], self.gates[swap2] = self.gates[swap2], self.gates[swap1]
        return ",".join(sorted(swaps))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 2024 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
