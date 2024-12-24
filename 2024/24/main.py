import itertools
import time

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

    def eval(self, out):
        if out in self.wires:
            return self.wires[out]
        a, op, b = self.gates[out].split()
        match op:
            case "AND":
                v = self.eval(a) & self.eval(b)
            case "OR":
                v = self.eval(a) | self.eval(b)
            case "XOR":
                v = self.eval(a) ^ self.eval(b)
        self.wires[out] = v
        return v

    def part1(self):
        out = []
        for i in itertools.count():
            name = "z" + str(i).zfill(2)
            if name not in self.gates:
                break
            out.append(self.eval(name))
        self.z = int("".join(map(str, out[::-1])), 2)
        return self.z

    def visualize(self, mistakes):
        with open("graph.dot", "w") as f:
            f.write("digraph G {\n")
            for k, v in self.gates.items():
                a, op, b = v.split()
                f.write(f'"{a}" -> "{a}{op}{b}"\n')
                f.write(f'"{b}" -> "{a}{op}{b}"\n')
                f.write(f'"{a}{op}{b}" -> "{k}"\n')
                if k in mistakes:
                    f.write(f'"{k}" [color=red, style=filled, fillcolor=lightpink];\n')
            f.write("}")

    def part2(self):
        def match_pattern(node, pattern):
            if pattern == "*" or node not in self.gates:
                return set()
            a, op, b = self.gates[node].split()
            if pattern[0] != op:
                return {node}

            e_ab = match_pattern(a, pattern[1]) | match_pattern(b, pattern[2])
            e_ba = match_pattern(b, pattern[1]) | match_pattern(a, pattern[2])
            return min(
                e_ab, e_ba, key=len
            )  # THe minimum set of nodes that contribute to the mistake

        mistakes = set()
        for n in itertools.count(start=1):
            z = f"z{n:02}"
            if z not in self.gates:
                break
            prev = n - 1
            corresponding_x = f"x{n:02}"
            corresponding_y = f"y{n:02}"

            prev_x = f"x{prev:02}"
            prev_y = f"y{prev:02}"

            mistakes |= match_pattern(
                z,
                (
                    "XOR",
                    ("XOR", corresponding_x, corresponding_y),
                    (
                        "OR",
                        ("AND", prev_x, prev_y),
                        ("AND", ("XOR", prev_x, prev_y), "*"),
                    ),
                ),
            )

        # self.visualize(mistakes)
        print(mistakes)

        known_false_positive = {"z45", "drq"}  # All the way in the beginning and end
        """
        By observation of the dot graph, we can see that the only way to make z16 correct,
        is if rpb gets its input from an AND gate that's connected to x15 and y15,
        and for ctg to get its input from an XOR gate (from x15 and y15), such that z15
        will get its correct output, and such that the output of ctg is correctly sent down
        to z16 (and onwards). Therefore, ctg and rpb need to be swapped, and vsd and wmb
        are false positives. (See graph.png)
        """
        visual_false_positive = {"wmb", "vsd"}
        visual_false_negative = {"rpb"}
        swaps = (
            mistakes - known_false_positive - visual_false_positive
            | visual_false_negative
        )
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
