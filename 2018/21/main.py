import time

# from Computer import Computer


def parseLines(lines):
    ip_index = int(lines[0].split(" ")[-1])

    return ip_index, [
        [opcode, int(a), int(b), int(c)]
        for opcode, a, b, c in [line.split(" ") for line in lines[1:]]
    ]


class Solution:
    def __init__(self):
        self.ip_index, self.data = parseLines(open("input.txt").read().rstrip().split("\n"))

        # Can use Computer.py with self.ip_index and data to find part1

    def part1(self):
        a = b = c = d = e = ip = 0

        while True:
            d = e | 65536
            e = 14464005
            while True:
                c = d & 255
                e += c
                e &= 16777215
                e *= 65899
                e &= 16777215
                if d < 256:
                    return e
                d //= 256

    def part2(self):
        a = b = c = d = e = ip = 0
        seen = set()
        prev_time = time.time()
        prev = -1

        while True:
            d = e | 65536
            e = 14464005
            while True:
                c = d & 255
                e += c
                e &= 16777215
                e *= 65899
                e &= 16777215
                if d < 256:
                    if time.time() - prev_time >= 0.1:
                        return prev
                    if e not in seen:
                        prev_time = time.time()
                        prev = e
                    seen.add(e)
                    break
                d //= 256


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
