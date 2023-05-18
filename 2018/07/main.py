import itertools
import re
from toposort import toposort


def parseLine(line):
    return tuple(re.findall(r"tep (\w)", line))[::-1]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.letter_dependant_on = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]
        self.unique = set(
            [letter for letter, _ in self.letter_dependant_on]
            + [dependant for _, dependant in self.letter_dependant_on]
        )
        self.delay = 0 if self.test else 60
        self.workers_count = 2 if self.test else 5

        self.dict = {
            frm: {to for frm2, to in self.letter_dependant_on if frm2 == frm}
            for frm, _ in self.letter_dependant_on
        }

    def part1(self):
        new_dict = self.dict
        topo = list(toposort(new_dict))
        out = ""
        while sum(len(sub) for sub in topo) > 1:
            topo = list(toposort(new_dict))

            for s in topo:
                nxt = min(s)
                out += nxt
                for value in new_dict.values():
                    if nxt in value:
                        value.remove(nxt)
                if nxt in new_dict:
                    del new_dict[nxt]
                break

        return out

    def part2(self):
        new_dict = {
            frm: {to for frm2, to in self.letter_dependant_on if frm2 == frm}
            for frm, _ in self.letter_dependant_on
        }
        complete = set()

        workers = []
        for second in itertools.count():
            # One second passes
            workers = [(letter, time_left - 1) for letter, time_left in workers if time_left > 0]

            for letter, time_left in workers:
                if time_left == 0:
                    complete.add(letter)

                    # Get rid of the letter from the dict...
                    for value in new_dict.values():
                        if letter in value:
                            value.remove(letter)
                    if letter in new_dict:
                        del new_dict[letter]
            # ... and worker-list
            workers = [worker for worker in workers if worker[1] > 0]

            if len(complete) == len(self.unique):
                return second

            # Get available letters
            for letter in next(toposort(new_dict)):
                # If we can start another worker and the letter is not worked on right now
                if len(workers) < self.workers_count and all(letter != c for c, _ in workers):
                    workers.append((letter, self.delay + 1 + ord(letter) - ord("A")))


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
