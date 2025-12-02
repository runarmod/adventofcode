import itertools
import re
import time

from aoc_utils_runarmod import get_data


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(2025, 2, test=test).strip("\n")

        self.data = nums(data)
        self.data = list(itertools.batched(self.data, 2))

    def part1(self):
        s = 0
        for r in self.data:
            for ID in range(r[0], r[1] + 1):
                id_string = str(ID)
                if id_string[: len(id_string) // 2] == id_string[len(id_string) // 2 :]:
                    s += ID
        return s

    def part2(self):
        s = 0
        for r in self.data:
            for ID in range(r[0], r[1] + 1):
                id_string = str(ID)
                for chunk_length in range(1, len(id_string)):
                    parts = len(id_string) // chunk_length
                    if len(id_string) % chunk_length != 0:
                        continue

                    chunk = id_string[:chunk_length]
                    if chunk * parts == id_string:
                        s += ID
                        break
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 1227775554 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 4174379265 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
