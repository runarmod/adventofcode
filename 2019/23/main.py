import time
from itertools import cycle

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))

    def part1(self):
        computers = [IntcodeComputer(self.data, i) for i in range(50)]
        for computer in cycle(computers):
            computer.run_until_io()
            for address, X, Y in computer.get_all_outputs():
                if address == 255:
                    return Y
                computers[address].push_input(X, Y)

    def part2(self):
        computers = [IntcodeComputer(self.data, i) for i in range(50)]
        NAT = None
        prev = None
        while True:
            for computer in computers:
                computer.run_until_io()
                for address, X, Y in computer.get_all_outputs():
                    if address == 255:
                        NAT = (X, Y)
                    else:
                        computers[address].push_input(X, Y)
            if all(computer.idle for computer in computers) and NAT is not None:
                if prev == NAT[1]:
                    return prev
                prev = NAT[1]
                computers[0].push_input(*NAT)


def main():
    start = time.perf_counter()

    solution = Solution()
    print(part1_text := f"Part 1: {solution.part1()}")
    print(part2_text := f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
