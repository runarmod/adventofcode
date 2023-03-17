import functools
import re
from collections import defaultdict
from copy import copy


def parseLine(line):
    if line.startswith("value"):
        return tuple(map(int, re.findall(r"(\d+)", line)))
    match = re.findall(r".*?(\d+).*?(\w+) (\d+).*?(\w+) (\d+)", line)[0]
    return (*map(int, [match[0], match[2], match[4]]), match[1], match[3])


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]

        self.dicts = {"output": defaultdict(list), "bot": defaultdict(list)}
        self.run()

    def part1(self):
        return self.part1_answer

    def part2(self):
        return functools.reduce(
            lambda x, y: x * y, (self.dicts["output"][i][0] for i in range(3)), 1
        )

    def run(self):
        self.dicts = {"output": defaultdict(list), "bot": defaultdict(list)}
        liste = copy(self.data)
        while liste:
            i = 0
            while i < len(liste):
                line = liste[i]
                if len(line) == 2:
                    self.dicts["bot"][line[1]].append(line[0])
                    liste.pop(i)
                elif len(self.dicts["bot"][line[0]]) >= 2:
                    (
                        bot,
                        recieve_min,
                        recieve_max,
                        recieve_min_output_type,
                        recieve_max_output_type,
                    ) = line

                    test_nrs = (5, 2) if self.test else (17, 61)
                    if all(test_nr in self.dicts["bot"][bot] for test_nr in test_nrs):
                        self.part1_answer = bot

                    minimum = min(self.dicts["bot"][bot])
                    maximum = max(self.dicts["bot"][bot])

                    self.dicts[recieve_min_output_type][recieve_min].append(minimum)
                    self.dicts[recieve_max_output_type][recieve_max].append(maximum)

                    self.dicts["bot"][bot].clear()
                    liste.pop(i)
                else:
                    i += 1


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
