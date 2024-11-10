import string


class Solution:
    def __init__(self):
        filename = "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split("-")))

    def generate_passwords(self, part):
        for i in range(self.data[0], self.data[1]):
            s = str(i)
            if s != "".join(sorted(s)):
                continue
            if len(s) <= len(set(s)):
                continue
            if part == 2 and not any(s.count(d) == 2 for d in string.digits):
                continue
            yield i

    def part1(self):
        return len(list(self.generate_passwords(part=1)))

    def part2(self):
        return len(list(self.generate_passwords(part=2)))


def main():
    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
