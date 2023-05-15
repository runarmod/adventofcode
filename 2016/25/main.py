import time


class Solution:
    def __init__(self):
        filename = "input.txt"
        self.data = [line.split(" ") for line in open(filename).read().rstrip().split("\n")]
        self.start_number = int(self.data[1][1]) * int(self.data[2][1])

    def part1(self):
        bin_rep = bin(self.start_number)[2:]
        correct = "10" * (len(bin_rep) // 2)

        # Our number may be too big to be represented as 1010..10 with same binary length
        if bin_rep[1] == "1":
            correct += "10"
        return int(correct, 2) - self.start_number


def main():
    start = time.perf_counter()

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
