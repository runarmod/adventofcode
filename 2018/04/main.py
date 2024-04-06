from collections import defaultdict
import itertools
import re
import string
import pprint
from datetime import datetime


def parseLine(line):
    date, thing, number = re.findall(
        r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (Guard #(\d+) begins shift|falls asleep|wakes up)",
        line,
    )[0]
    date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    if number:
        return (date, thing, int(number))
    return (date, thing)


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = sorted(
            [parseLine(line) for line in open(filename).read().rstrip().split("\n")],
            key=lambda x: x[0],
        )
        self.guards = defaultdict(lambda: {"minutes": defaultdict(int), "total": 0})

    def part1(self):
        for line in self.data:
            if "Guard" in line[1]:
                guard = line[2]
            elif "falls" in line[1]:
                start = line[0].minute
            else:
                end = line[0].minute
                for i in range(start, end):
                    self.guards[guard]["minutes"][i] += 1
                self.guards[guard]["total"] += end - start
        longest = max(self.guards, key=lambda guard: self.guards[guard]["total"])

        minute_most = max(
            self.guards[longest]["minutes"],
            key=lambda x: self.guards[longest]["minutes"][x],
        )

        return minute_most * longest

    def part2(self):
        for line in self.data:
            if "Guard" in line[1]:
                guard = line[2]
            elif "falls" in line[1]:
                start = line[0].minute
            else:
                end = line[0].minute
                for i in range(start, end):
                    self.guards[guard]["minutes"][i] += 1

        for guard, data in self.guards.items():
            data["minute_most"] = max(data["minutes"], key=lambda x: data["minutes"][x])
            data["minute_most_count"] = data["minutes"][data["minute_most"]]

        longest = max(
            self.guards, key=lambda guard: self.guards[guard]["minute_most_count"]
        )
        return (
            max(
                self.guards[longest]["minutes"],
                key=lambda x: self.guards[longest]["minutes"][x],
            )
            * longest
        )


def main():
    test = Solution(test=True)
    print(part1_test := f"Part 1: {test.part1()}")
    print(part2_test := f"Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
