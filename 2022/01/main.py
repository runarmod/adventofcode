from heapq import heapify


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [-sum(int(calorie) for calorie in raindeer.split("\n")) for raindeer in open(filename).read().rstrip().split("\n\n")]

        heapify(self.data)


    def part1(self):
        return abs(self.data[0])

    def part2(self):
        return abs(sum(self.data[:3]))


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
