from collections import Counter, defaultdict


def parseLine(line):
    k, v = line.split(" -> ")
    return k, v


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.poly, recipes = open(filename).read().rstrip().split("\n\n")

        self.data = {}
        for line in recipes.split("\n"):
            k, v = parseLine(line)
            self.data[k] = v

        self.rules = {a: (a[0] + c, c + a[1]) for a, c in self.data.items()}
        self.pairs = ["".join(p) for p in zip(self.poly, self.poly[1:])]

    def run(self, iterations):
        ctr = Counter(self.pairs)
        for _ in range(iterations):
            newCtr = {k: 0 for k in self.data.keys()}
            for k, v in ctr.items():
                newCtr[self.rules[k][0]] += v
                newCtr[self.rules[k][1]] += v
            ctr = newCtr

        count = defaultdict(int)
        for k, v in ctr.items():
            count[k[0]] += v
        count[self.poly[-1]] += 1

        return count[max(count, key=lambda x: count[x])] - count[min(count, key=lambda x: count[x])]

    def part1(self):
        return self.run(10)

    def part2(self):
        return self.run(40)


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
