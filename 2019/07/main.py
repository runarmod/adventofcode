from IntcodeComputer import IntcodeComputer
import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split(",")))

    def part1(self):
        best = 0
        for inputs in itertools.permutations(range(5)):
            prev_computer = IntcodeComputer(self.data)
            for phase in inputs:
                computer = IntcodeComputer(self.data)
                computer.inputs.append(phase)
                if prev_computer.output is None:
                    computer.inputs.append(0)
                else:
                    computer.inputs.append(prev_computer.output)
                computer.run()
                prev_computer = computer

            best = max(best, prev_computer.output)
        return best

    def part2(self):
        best = 0

        for inputs in itertools.permutations(range(5, 10)):
            computers = [IntcodeComputer(self.data) for _ in range(5)]
            for computer, phase in zip(computers, inputs):
                computer.inputs.append(phase)

            prev_out = 0
            while all(not computer.halted for computer in computers):
                for computer in computers:
                    computer.inputs.append(prev_out)
                    output = computer.run()
                    if not computer.halted:
                        prev_out = output
                    computer.inputs.clear()
            best = max(best, prev_out)
        return best


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test2 = test.part2()
    print(
        f"(TEST) Part 2: {test2}, {'correct :)' if test2 == 139629729 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
