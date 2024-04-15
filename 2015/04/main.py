import itertools
import multiprocessing
import time
from hashlib import md5

from more_itertools import consume


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.prefix = open(filename).read().rstrip()

    def correct_number(self, number, leading_zeros):
        return (
            md5((self.prefix + str(number)).encode(), usedforsecurity=False)
            .hexdigest()
            .startswith("0" * leading_zeros)
        )

    def find_hash(
        self, leading_zeros, process_nr=1, threads=1, out=multiprocessing.Queue
    ):
        for i in itertools.count(
            start=process_nr,
            step=threads,
        ):
            if self.correct_number(i, leading_zeros):
                out.put(i)
                return i

    def find_hash_threaded(self, leading_zeros):
        threads = multiprocessing.cpu_count() - 1
        out = multiprocessing.Queue()

        processes = [
            multiprocessing.Process(
                target=self.find_hash,
                args=(leading_zeros, i, threads, out),
            )
            for i in range(threads)
        ]

        consume(map(lambda p: p.start(), processes))

        result = out.get()

        for process in processes:
            process.terminate()
        return result

    def part1(self):
        # return self.find_hash(5) # <-- With no multiprocessing
        return self.find_hash_threaded(5)

    def part2(self):
        # return self.find_hash(6) # <-- With no multiprocessing
        return self.find_hash_threaded(6)


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
