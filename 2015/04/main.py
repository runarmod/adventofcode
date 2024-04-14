import hashlib
import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()

    def find_hash(self, leading_zeros):
        for i in itertools.count():
            word = self.data + str(i)
            hash = hashlib.md5(word.encode(), usedforsecurity=False).hexdigest()
            if hash.startswith("0" * leading_zeros):
                return i

    def part1(self):
        return self.find_hash(5)

    def part2(self):
        return self.find_hash(6)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1},\t{'correct :)' if test1 == 609043 else 'wrong :('}")
    print(
        f"(TEST) Part 2: {test2},\t{'correct :)' if test2 == 6742839 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
