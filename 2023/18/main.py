import time
from collections import deque


def parseLine(line):
    d, l, c = line.split(" ")
    return d, int(l), c[2:-1]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def old_part1(self):
        m = set()
        x, y = 0, 0
        for _dir, length, _ in self.data:
            match _dir:
                case "R":
                    for _ in range(length):
                        x += 1
                        m.add((x, y))
                case "L":
                    for _ in range(length):
                        x -= 1
                        m.add((x, y))
                case "U":
                    for _ in range(length):
                        y -= 1
                        m.add((x, y))
                case "D":
                    for _ in range(length):
                        y += 1
                        m.add((x, y))

        q = deque()
        q.append((1, 1))  # I saw that (1, 1) was inside in both test and real
        while q:
            x, y = q.popleft()
            if (x, y) in m:
                continue
            m.add((x, y))
            q.append((x + 1, y))
            q.append((x - 1, y))
            q.append((x, y + 1))
            q.append((x, y - 1))
        return len(m)

    def shoelace(self, x, y, perim):
        return (
            abs(
                sum(i * j for i, j in zip(x, y[1:] + y[:1]))
                - sum(i * j for i, j in zip(x[1:] + x[:1], y))
            )
            // 2
            + perim // 2
            + 1
        )

    def run(self, dirs, lengths):
        m = [(0, 0)]
        x, y = 0, 0
        perim = 0
        for _dir, length in zip(dirs, lengths):
            perim += length
            match _dir:
                case "R":
                    x += length
                case "L":
                    x -= length
                case "U":
                    y -= length
                case "D":
                    y += length
            m.append((x, y))
        return self.shoelace(*zip(*m), perim)

    def part1(self):
        return self.run(*zip(*((x[0], x[1]) for x in self.data)))

    def part2(self):
        return self.run(
            ("RDLU"[int(h[-1])] for _, _, h in self.data),
            (int(h[:-1], 16) for _, _, h in self.data),
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1},\t\t{'correct :)' if test1 == 62 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2},\t{'correct :)' if test2 == 952408144115 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
