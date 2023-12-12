import time


def parseLine(line):
    return line.replace("(", "( ").replace(")", " )").strip().split()


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def eval1(self, line):
        assert "(" not in line
        assert ")" not in line

        while len(line) != 1:
            line = [str(eval("".join(line[:3])))] + line[3:]
        return int(line[0])

    def eval2(self, line):
        assert "(" not in line
        assert ")" not in line

        while "+" in line:
            i = next((i for i, c in enumerate(line) if c == "+"), -1)
            assert i != -1
            line = (
                line[: i - 1]
                + [str(eval("".join(line[i - 1 : i + 2])))]
                + line[i + 2 :]
            )
        return eval("".join(line))

    def run(self, eval_fn):
        s = 0
        for line in self.data:
            while "(" in line:
                left = -1
                right = -1
                for i in range(len(line)):
                    if line[i] == "(":
                        left = i
                    elif line[i] == ")":
                        right = i
                        break
                assert left != -1
                line = (
                    line[:left]
                    + [str(eval_fn(line[left + 1 : right]))]
                    + line[right + 1 :]
                )
            s += eval_fn(line)
        return s

    def part1(self):
        return self.run(self.eval1)

    def part2(self):
        return self.run(self.eval2)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 26+437+12240+13632 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 46+1445+669060+23340 else 'wrong :('}"
    )

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
