import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()

    def part1(self):
        return self.data.count("(") - self.data.count(")")

    def part2(self):
        counter = 0
        for i in range(len(self.data)):
            if self.data[i] == "(":
                counter += 1
            elif self.data[i] == ")":
                counter -= 1
            if counter < 0:
                return i + 1


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 3 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 1 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
