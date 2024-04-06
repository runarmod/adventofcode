import re
from collections import defaultdict


class Solution():
    def __init__(self, test=False):
        self.test = test
        self.finished = 1000 if test else 2503
        filename = "testinput.txt" if self.test else "input.txt"
        self.pattern = re.compile(
            r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.")
        self.data = [(name, int(speed), int(work), int(rest)) for name, speed,
                     work, rest in self.pattern.findall(open(filename).read().rstrip())]

        self.deer = defaultdict(dict)
        for name, _, _, _ in self.data:
            self.deer[name]["dist"] = 0
            self.deer[name]["points"] = 0



    def part1(self):
        record = 0
        for _, speed, work, rest in self.data:
            totalTime = 0
            distance = 0
            while totalTime < self.finished:
                if totalTime % (work + rest) < work:
                    distance += speed
                totalTime += 1
            record = max(record, distance)
        return record

    def part2(self):
        maxDist = 0
        for totalTime in range(self.finished):
            for name, speed, work, rest in self.data:
                if totalTime % (work + rest) < work:
                    self.deer[name]["dist"] += speed
            maxDist = max(self.deer[name]["dist"] for name in self.deer)
            for name, value in self.deer.items():
                if value["dist"] == maxDist:
                    self.deer[name]["points"] += 1
        return max(self.deer[name]["points"] for name in self.deer)


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
