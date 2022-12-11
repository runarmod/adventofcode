from copy import deepcopy
import math
import re
import functools


def parseMonkey(monkey):
    lines = monkey.split("\n")
    monkey_nr = int(lines[0].split(" ")[1][:-1])
    starting_items = list(map(int, lines[1].split(": ")[1].split(", ")))
    test = int(re.findall(r"(\d+)", lines[3])[0])
    true = int(re.findall(r"(\d+)", lines[4])[0])
    false = int(re.findall(r"(\d+)", lines[5])[0])

    function = lines[2].split(" = ")[1].split("old ")[1]
    newOp = function.split(" ")[1]
    if function == "* old":
        function = lambda x: pow(x, 2)
    elif function[0] == "*":
        function = lambda x: x * int(newOp)
    elif function[0] == "+":
        function = lambda x: x + int(newOp)

    return {
        "inspect_count": 0,
        "monkey_nr": monkey_nr,
        "items": starting_items,
        "function": function,
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
        self.lcm = math.lcm(*[self.data[i]["test"] for i in range(len(self.data))])

    def part1(self):
        part_1_data = self.run(deepcopy(self.data), 20)
        return self.calculate_score(part_1_data)

    def part2(self):
        part_2_data = self.run(deepcopy(self.data), 10000)
        return self.calculate_score(part_2_data)

    def monkey_round(self, monkey_nr, data, part1=False):
        for item in data[monkey_nr]["items"]:
            self.calculate_worry(monkey_nr, data, part1, item)
        data[monkey_nr]["items"] = []
        return data

    def calculate_worry(self, monkey_nr, data, part1, item):
        data[monkey_nr]["inspect_count"] += 1

        worry = data[monkey_nr]["function"](item)
        if part1:
            worry //= 3
        else:
            worry %= self.lcm

        true_false = "false" if worry % data[monkey_nr]["test"] else "true"
        data[data[monkey_nr][true_false]]["items"].append(worry)

    def run(self, data, length):
        for _ in range(length):
            for i in range(len(data)):
                data = self.monkey_round(i, data)
        return data

    def calculate_score(self, data):
        return functools.reduce(
            lambda x, y: x * y,
            sorted([i["inspect_count"] for i in data], reverse=True)[:2],
        )


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


if __name__ == "__main__":
    main()
