import re
import time


def parseLine(line) -> tuple[str, tuple[int]]:
    line = line.split()
    return line[0], tuple(map(int, re.findall(r"\d+", line[1])))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def _count(
        self,
        kart: str,
        remaining: tuple[int],
        i: int,
        block_i: int,
        curr_length: int,
    ) -> int:
        # State is position in line, position in remaining blocks, current length of block
        # This is a unique state and as general as possible
        if (i, block_i, curr_length) in self.DP:
            return self.DP[(i, block_i, curr_length)]

        if i == len(kart):
            # If we are at the end of the line, we are done if we have no more blocks to take
            if block_i == len(remaining) and curr_length == 0:
                return 1
            # If we only have one block left, we are done if we have the correct length,
            # else this didnt work
            return block_i == len(remaining) - 1 and curr_length == remaining[block_i]

        answer = 0

        # Don't take more / finish taking
        if kart[i] in ".?":
            if curr_length == 0:
                # Keep *not taking*
                answer += self._count(kart, remaining, i + 1, block_i, 0)
            elif (
                curr_length > 0
                and block_i < len(remaining)
                and remaining[block_i] == curr_length
            ):
                # Finish taking
                answer += self._count(kart, remaining, i + 1, block_i + 1, 0)

        # Take new
        if kart[i] in "?#":
            answer += self._count(kart, remaining, i + 1, block_i, curr_length + 1)

        self.DP[(i, block_i, curr_length)] = answer
        return answer

    def count(self, kart: str, rem: tuple[int]) -> int:
        self.DP = {}
        return self._count(kart, rem, 0, 0, 0)

    def part1(self):
        return sum(self.count(kart, rem) for kart, rem in self.data)

    def part2(self):
        return sum(
            self.count("?".join(kart for _ in range(5)), rem * 5)
            for kart, rem in self.data
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 21 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 525152 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
