class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.start = tuple(map(int, open(filename).read().rstrip().split(",")))

    def part1(self):
        return self.run(2020)

    def part2(self):
        return self.run(30000000)

    def run(self, length):
        visited = set()
        data = {}
        latest = -1

        for rip in range(length):
            if rip < len(self.start):
                nxt = self.start[rip]
            else:
                nxt = 0 if latest not in visited else rip - data[latest]
            data[latest] = rip
            visited.add(latest)

            latest = nxt
        return nxt


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    sol = Solution()
    print(f"Part 1: {sol.part1()}")
    print(f"Part 2: {sol.part2()}")


if __name__ == "__main__":
    main()
