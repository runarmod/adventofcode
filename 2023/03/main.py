import itertools
import re
import time
from collections import defaultdict


def parseLine(line, y):
    line = "".join(line)
    matches = re.finditer(r"\d+", line)
    out = []
    count_dict = defaultdict(int)
    for mat in matches:
        start = mat.start()
        number = mat.group()
        end = start + len(number)

        count_dict[number] += 1
        dictionary = {
            "match": int(number),
            "neighbors": [],
        }
        for x in range(start, end):
            for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                if (
                    x + dx < 0
                    or x + dx >= len(line)
                    or y + dy < 0
                    or y + dy >= len(line)
                ):
                    continue
                dictionary["neighbors"].append((x + dx, y + dy))
        out.append(dictionary)
    return out


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.graph = [list(line) for line in open(filename).read().rstrip().split("\n")]
        tmp_data = [parseLine(line, y) for y, line in enumerate(self.graph)]
        self.data = list(itertools.chain(*tmp_data))

    def fun(self, data):
        for x, y in data["neighbors"]:
            if self.graph[y][x] != "." and not self.graph[y][x].isdigit():
                return data["match"]
        return 0

    def part1(self):
        return sum(self.fun(data) for data in self.data)

    def part2(self):
        _sum = 0
        for y, x in itertools.product(
            range(len(self.graph)), range(len(self.graph[0]))
        ):
            if self.graph[y][x] != "*":
                continue
            numbers = []
            for num in self.data:
                if (x, y) in num["neighbors"]:
                    numbers.append(num["match"])
            if len(numbers) == 2:
                _sum += numbers[0] * numbers[1]
        return _sum


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
