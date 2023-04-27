from math import ceil
from operator import mul


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        first, busses = open(filename).read().rstrip().split("\n")
        self.first = int(first)
        self.busses = list(map(int, (x for x in busses.split(",") if x != "x")))
        self.delay_busnr = [(i, int(bus)) for i, bus in enumerate(busses.split(",")) if bus != "x"]

    def part1(self):
        return mul(*min((ceil(self.first / bus) * bus - self.first, bus) for bus in self.busses))

    def part2(self):
        multiple, ans = 1, 0
        for delay, bus_nr in self.delay_busnr:
            while (ans + delay) % bus_nr != 0:
                ans += multiple
            multiple *= bus_nr
        return ans


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
