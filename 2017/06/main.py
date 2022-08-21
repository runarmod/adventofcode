class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip().split("\t")))

    def part1(self):
        data = self.data[:]
        seen = set()
        while True:
            seen.add(tuple(data))
            maxval = max(data)
            maxidx = data.index(maxval)
            data[maxidx] = 0
            for i in range(1, maxval + 1):
                data[(maxidx + i) % len(data)] += 1
            if tuple(data) in seen:
                return len(seen)

    def part2(self):
        data = self.data[:]
        seen = set()
        find = None
        while True:
            seen.add(tuple(data))
            maxval = max(data)
            maxidx = data.index(maxval)
            data[maxidx] = 0
            for i in range(1, maxval + 1):
                data[(maxidx + i) % len(data)] += 1
            if tuple(data) in seen:
                find = tuple(data)
                break
        counter = 0
        while True:
            counter += 1
            maxval = max(data)
            maxidx = data.index(maxval)
            data[maxidx] = 0
            for i in range(1, maxval + 1):
                data[(maxidx + i) % len(data)] += 1
            if tuple(data) == find:
                return counter


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    if not solution.test:
        with open("solution.txt", "w") as f:
            f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
