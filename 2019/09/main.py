from IntcodeComputer import IntcodeComputer
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split(",")))

    def part1(self):
        computer = IntcodeComputer(self.data)
        computer.inputs.append(1)
        return computer.run()

    def part2(self):
        computer = IntcodeComputer(self.data)
        computer.inputs.append(2)
        return computer.run()


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1}, {'correct :)' if test1 == 1219070632396864 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
