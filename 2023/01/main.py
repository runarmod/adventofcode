import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")

    def part1(self):
        s = 0
        for line in self.data:
            l = ""
            for c in line:
                if "0" <= c <= "9":
                    l += c
                    break
            for c in line[::-1]:
                if "0" <= c <= "9":
                    l += c
                    break
            s += int(l)
        return s

    def nxt(self, line, _range):
        d = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        for i in _range:
            for k, v in d.items():
                if "".join(line[i:]).startswith(k):
                    return str(v)
            if "0" <= line[i] <= "9":
                return line[i]
        return None

    def part2(self):
        s = 0
        for line in self.data:
            l = self.nxt(line, range(len(line)))
            l += self.nxt(line, range(len(line) - 1, -1, -1))
            s += int(l)
        return s


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
