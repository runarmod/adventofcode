import time
from collections import defaultdict


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().strip().split(",")

    def hash_word(self, word):
        counter = 0
        for char in word:
            counter = self.hash_char(char, counter)
        return counter

    def hash_char(self, char, initial):
        return ((initial + ord(char)) * 17) % 256

    def part1(self):
        return sum(self.hash_word(s) for s in self.data)

    def score(self, dictionary):
        return sum(
            (box + 1) * (slot + 1) * box_element[1]
            for box, values in dictionary.items()
            for slot, box_element in enumerate(values)
        )

    def part2(self):
        d = defaultdict(list)
        for word in self.data:
            real_word = (
                word[: word.index("-")] if "-" in word else word[: word.index("=")]
            )

            num = self.hash_word(real_word)

            if "-" in word:
                d[num] = [c for c in d[num] if c[0] != real_word]
            elif "=" in word:
                i = int(word.split("=")[-1])
                if real_word not in (c[0] for c in d[num]):
                    d[num].append((real_word, i))
                else:
                    d[num] = [
                        c if c[0] != real_word else (real_word, i) for c in d[num]
                    ]
            else:
                assert False, f"{word=}, {num=}"
        return self.score(d)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 1320 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 145 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
