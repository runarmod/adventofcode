import functools
from hashlib import md5
import re


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.salt = open(filename).read().rstrip()

    @functools.lru_cache(maxsize=0)
    def hash(self, string):
        return md5(string.encode(), usedforsecurity=False).hexdigest()

    @functools.lru_cache(maxsize=0)
    def stretched_hash(self, string):
        _hash = string
        for _ in range(2017):
            _hash = md5(_hash.encode(), usedforsecurity=False).hexdigest()
        return _hash

    def run(self, fn):
        triple = re.compile(r"(\w)\1{2}")
        quintuple = re.compile(r"(\w)\1{4}")

        found = set()
        index_nr = 0
        while len(found) < 78:  # Buffer så vi er sikker på at vi ikke finner noen senere tidligere
            _hash = fn(f"{self.salt}{index_nr}")
            for quin_hash_char in set(quintuple.findall(_hash)):
                for triple_idx in range(max(index_nr - 1000, 0), index_nr):
                    returned_hash = fn(f"{self.salt}{triple_idx}")
                    triple_hash_char = triple.search(returned_hash)

                    if triple_hash_char and quin_hash_char == triple_hash_char[1]:
                        found.add(triple_idx)
                        # print(f"Found {triple_idx}")
            index_nr += 1
        return sorted(found)[63]

    def part1(self):
        return self.run(self.hash)

    def part2(self):
        return self.run(self.stretched_hash)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
