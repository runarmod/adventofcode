import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip()))
        self.pattern = [0, 1, 0, -1]

    def get_pattern(self, idx):
        first = True
        for i in itertools.count():
            for j in range(idx + 1):
                if first and j == 0:
                    first = False
                    continue
                yield self.pattern[i % len(self.pattern)]

    def part1(self):
        nums = self.data
        for _ in range(100):
            new_nums = []
            for digit_index in range(len(nums)):
                s = 0
                for digit_pattern, digit_input in zip(
                    itertools.islice(self.get_pattern(digit_index), len(nums)), nums
                ):
                    s += digit_input * digit_pattern
                new_nums.append(abs(s) % 10)
            nums = new_nums
        return int("".join(map(str, nums[:8])))

    def part2(self):
        nums = self.data * 10_000
        offset = int("".join(map(str, nums[:7])))
        for _ in range(100):
            for i in range(len(nums) - 1, offset, -1):
                nums[i - 1] = (nums[i - 1] + nums[i]) % 10
        return int("".join(map(str, nums[offset : offset + 8])))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 24465799 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 84462026 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
