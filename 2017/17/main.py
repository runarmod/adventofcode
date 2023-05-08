from collections import deque


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.steps = int(open(filename).read().strip())

    def part1(self):
        spinlock = deque([0])
        for i in range(1, 2018):
            spinlock.rotate(-self.steps)
            spinlock.append(i)
        return spinlock[(spinlock.index(2017) + 1) % len(spinlock)]

    def part2(self):
        spinlock = deque([0])
        for i in range(1, 50_000_000):
            spinlock.rotate(-self.steps)
            spinlock.append(i)
        return spinlock[spinlock.index(0) + 1]


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
