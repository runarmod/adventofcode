from collections import deque


def parseLine(line):
    return tuple(map(int, line.split(",")))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = {
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        }

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)

    def check(self, x, y, z, part):
        if (x, y, z) in self.inn:
            return False
        if (x, y, z) in self.out:
            return True

        temp = set()
        q = deque([(x, y, z)])
        while q:
            x, y, z = q.popleft()
            if (x, y, z) in self.data:
                continue
            if (x, y, z) in temp:
                continue

            temp.add((x, y, z))
            if len(temp) > (1500 if part == 2 else 0):
                self.out |= temp
                return True

            dirs = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0))
            for x_c, y_c, z_c in dirs:
                q.append((x + x_c, y + y_c, z + z_c))
        self.inn |= temp

    def run(self, part):
        self.inn = set()
        self.out = set()
        s = 0
        dirs = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0))
        for x, y, z in self.data:
            for x_c, y_c, z_c in dirs:
                if self.check(x + x_c, y + y_c, z + z_c, part):
                    s += 1
        return s


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
