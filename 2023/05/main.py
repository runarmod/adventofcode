import time


def parseData(data):
    data = data.split("\n\n")
    seeds = list(map(int, data[0].split(": ")[1].split(" ")))
    data = [d.split("\n")[1:] for d in data[1:]]
    data = [list(tuple(map(int, d.split(" "))) for d in section) for section in data]
    return seeds, data


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.seeds, self.data = parseData(open(filename).read().rstrip())

    def part1(self):
        m = {seed: seed for seed in self.seeds}
        for section in self.data:
            moved = set()
            for dest, src, ran in section:
                for seed, loc in m.items():
                    if seed not in moved and src <= loc < src + ran:
                        m[seed] = dest + (loc - src)
                        moved.add(seed)
        return min(v for v in m.values())

    def part2(self):
        ranges_to_check = [
            range(self.seeds[i], self.seeds[i] + self.seeds[i + 1])
            for i in range(0, len(self.seeds), 2)
        ]

        for section in self.data:
            new_ranges: set[range] = set()
            i = 0
            while i < len(ranges_to_check):
                current = ranges_to_check[i]
                success = False
                for destination, start, length in section:
                    stop = start + length
                    offset = destination - start  # newPos = oldPost + offset

                    if stop <= current.start or current.stop < start:
                        # The map doesnt say anything about the range
                        continue

                    inner = range(max(current.start, start), min(current.stop, stop))
                    new_ranges.add(range(inner.start + offset, inner.stop + offset))

                    left = range(current.start, inner.start)
                    if left.stop - left.start > 0 and left not in ranges_to_check:
                        ranges_to_check.append(left)

                    right = range(inner.stop, current.stop)
                    if right.stop - right.start > 0 and right not in ranges_to_check:
                        ranges_to_check.append(right)

                    success = True
                    break
                if not success:
                    new_ranges.add(current)
                i += 1
            ranges_to_check = list(new_ranges)

        return min(v.start for v in ranges_to_check)


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
