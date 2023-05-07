import functools
from operator import mul


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().strip()

        self.ascii_data = list(map(ord, self.data))
        if not test:
            self.lengths = list(map(int, self.data.split(",")))

        self.numbers = list(range(256))
        self.standard_suffix = [17, 31, 73, 47, 23]

    def round(
        self, index: int, skipsize: int, numbers: list[int], lengths: list[int]
    ) -> tuple[int, int, list[int]]:
        for length in lengths:
            _numbers = numbers[index:] + numbers[:index]
            rev = _numbers[:length][::-1]
            _numbers = rev + _numbers[length:]
            numbers = _numbers[-index:] + _numbers[:-index]
            index = (index + length + skipsize) % len(numbers)
            skipsize += 1
        return index, skipsize, numbers

    def part1(self) -> int:
        _, _, numbers = self.round(0, 0, self.numbers[:], self.lengths)

        return mul(*numbers[:2])

    def hash(self, lst: list[int]) -> list[int]:
        return [
            functools.reduce(lambda x, y: x ^ y, lst[i : i + 16], 0) for i in range(0, len(lst), 16)
        ]

    def part2(self) -> str:
        index = 0
        skipsize = 0
        numbers = self.numbers[:]
        length_seq = self.ascii_data + self.standard_suffix

        for _ in range(64):
            index, skipsize, numbers = self.round(index, skipsize, numbers, length_seq)
        dense_hash = self.hash(numbers)
        return "".join(hex(num)[2:].zfill(2) for num in dense_hash)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
