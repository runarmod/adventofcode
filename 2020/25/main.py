import itertools
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"

        # Doesn't matter the order of the pubs. The other way is faster for me, so I take the liberty
        self.pubs = list(map(int, open(filename).read().rstrip().split("\n")))[::-1]
        self.subject = 7

    def part1(self):
        return pow(
            self.pubs[1],
            (
                lambda num: next(
                    loop_size
                    for loop_size in itertools.count(start=1)
                    if (num := (num * self.subject) % 20201227) == self.pubs[0]
                )
            )(1),
            20201227,
        )
        # Produces only one loop_size


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 14897079 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
