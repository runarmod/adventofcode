from collections import defaultdict
from copy import deepcopy
from pprint import pprint
import itertools
import pyperclip
import re
import string
import functools
from tqdm import trange


def parseMonkey(monkey):
    lines = monkey.split("\n")
    monkey_nr = int(lines[0].split(" ")[1][:-1])
    starting_items = set(map(int, lines[1].split(": ")[1].split(", ")))
    operation = lines[2].split(" = ")[1].split("old ")[1]
    newOp = operation.split(" ")[1]
    # print(operation)
    
    if operation == "* old":
        operation = lambda x: x ** 2
    elif operation[0] == "*":
        operation = lambda x: x * int(newOp)
    elif operation[0] == "+":
        operation = lambda x: x + int(newOp)
    test = int(re.findall(r"(\d+)", lines[3])[0])
    true = int(re.findall(r"(\d+)", lines[4])[0])
    false = int(re.findall(r"(\d+)", lines[5])[0])
    return {
        "inspect_count": 0,
        "monkey_nr": monkey_nr,
        "items": starting_items,
        "operation": operation,
        "test": test,
        "true": true,
        "false": false,
    }


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseMonkey(line) for line in open(filename).read().rstrip().split("\n\n")
        ]

    def monkey_round(self, monkey_nr):
        for item in self.part_1_data[monkey_nr]["items"]:
            self.part_1_data[monkey_nr]["inspect_count"] += 1
            op = self.part_1_data[monkey_nr]["operation"]
            worry = op(item)
            worry //= 3
            # print(op)
            # worry = eval(str(item) + self.part_1_data[monkey_nr]["operation"]) // 3
            if worry % self.part_1_data[monkey_nr]["test"] == 0:
                self.part_1_data[self.part_1_data[monkey_nr]["true"]]["items"].add(
                    worry
                )
            else:
                self.part_1_data[self.part_1_data[monkey_nr]["false"]]["items"].add(
                    worry
                )
        self.part_1_data[monkey_nr]["items"] = set()

    def part1(self):
        self.part_1_data = deepcopy(self.data)
        for round in range(20):
            for i, monkey in enumerate(self.data):
                self.monkey_round(i)
        return functools.reduce(
            lambda x, y: x * y,
            sorted([i["inspect_count"] for i in self.part_1_data], reverse=True)[:2],
        )

    def monkey_round_2(self, monkey_nr):
        for item in self.part_2_data[monkey_nr]["items"]:
            self.part_2_data[monkey_nr]["inspect_count"] += 1
            op = self.part_2_data[monkey_nr]["operation"]
            worry = op(item)
            # worry = eval(str(item) + self.part_2_data[monkey_nr]["operation"])
            if worry % self.part_2_data[monkey_nr]["test"] == 0:
                self.part_2_data[self.part_2_data[monkey_nr]["true"]]["items"].add(
                    worry
                )
            else:
                self.part_2_data[self.part_2_data[monkey_nr]["false"]]["items"].add(
                    worry
                )
        self.part_2_data[monkey_nr]["items"] = set()

    def part2(self):
        self.part_2_data = deepcopy(self.data)
        for round in trange(10000):
            for i in range(len(self.part_2_data)):
                self.monkey_round_2(i)
        pprint(self.part_2_data)
        return functools.reduce(
            lambda x, y: x * y,
            sorted([i["inspect_count"] for i in self.part_2_data], reverse=True)[:2],
        )


def main():
    test = Solution(test=True)
    # print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    # part1 = solution.part1()
    part2 = solution.part2()
    # print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    # copy_answer(part1, part2)

    # with open("solution.txt", "w") as f:
    #     f.write(f"{part1_text}\n{part2_text}\n")


def copy_answer(part1, part2):
    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)


if __name__ == "__main__":
    main()
