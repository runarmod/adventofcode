import copy
import re


def parseLine(line):
    pattern = re.compile(r"(nop|acc|jmp) ([+-]\d+)")
    op, off = re.findall(pattern, line)[0]
    return op, int(off)


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]

        self.rip = 0
        self.acc = 0

    def inf_loop(self, data):
        rip = acc = 0
        visited = set()
        while rip < len(data):
            if rip in visited:
                return (True, acc)
            visited.add(rip)
            operation, offset = data[rip]
            match operation:
                case "nop":
                    rip += 1
                case "acc":
                    acc += offset
                    rip += 1
                case "jmp":
                    rip += offset
        return (False, acc)

    def part1(self):
        return self.inf_loop(self.data)[1]

    def part2(self):
        for i, line in enumerate(self.data):
            if line[0] not in ("nop", "jmp"):
                continue
            data = self.data.copy()
            data[i] = ("nop" if line[0] == "jmp" else "jmp", line[1])

            if not (ret := self.inf_loop(data))[0]:
                return ret[1]
        return "NOT FOUND"


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")


if __name__ == "__main__":
    main()
