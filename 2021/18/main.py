import itertools
import re
from math import ceil


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(open(filename).read().rstrip().split("\n"))

    def collapse(self, snail):
        depth = -1
        new_snail = ""
        for i, c in enumerate(snail):
            if c == ",":
                continue
            if c == "[":
                depth += 1
                continue
            if c == "]":
                depth -= 1
                continue
            if depth >= 4:
                remove = re.search(r"(\d+),(\d+)", snail[i:])
                break
        else:
            return False
        prev = re.findall(r"(\d+)", snail[:i])
        prev = prev[-1] if len(prev) > 0 else None

        nxt = re.search(r"(\d+)", snail[i + snail[i:].find("]") :])
        if prev is None:
            new_snail += snail[: i - 1]
        else:
            left_value = remove.string[remove.regs[1][0] : remove.regs[1][1]]
            new_snail += snail[: i - 1][::-1].replace(
                prev[::-1], str(int(prev) + int(left_value))[::-1], 1
            )[::-1]
        new_snail += "0"

        left_part = snail[i + snail[i:].find("]") + 1 :]
        if nxt is None:
            new_snail += left_part
        else:
            new_snail += left_part.replace(
                nxt[0],
                str(int(nxt[0]) + int(remove.string[remove.regs[2][0] : remove.regs[2][1]])),
                1,
            )
        return new_snail

    def split(self, snail):
        found = re.findall(r"(\d{2,})", snail)
        if len(found) == 0:
            return False
        found = found[0]
        replace = f"[{int(found) // 2},{ceil(int(found) / 2)}]"

        return snail.replace(found, replace, 1)

    def add(self, snail1, snail2):
        new_snail = f"[{snail1},{snail2}]"
        while True:
            if (s := self.collapse(new_snail)) != False:
                new_snail = s
                continue
            if (s := self.split(new_snail)) != False:
                new_snail = s
                continue
            break
        return new_snail

    def magnitude(self, snail):
        while snail.count(",") > 1:
            pair = re.findall(r"\[(\d+),(\d+)\]", snail)[0]
            snail = snail.replace(
                f"[{pair[0]},{pair[1]}]", f"{int(pair[0]) * 3 + int(pair[1]) * 2}"
            )
        left, right = snail[1:-1].split(",")
        return int(left) * 3 + int(right) * 2

    def part1(self):
        rolling_sum = self.data[0]
        for i in range(1, len(self.data)):
            rolling_sum = self.add(rolling_sum, self.data[i])
        return self.magnitude(rolling_sum)

    def part2(self):
        best = 0
        for first, last in itertools.permutations(self.data, 2):
            best = max(self.magnitude(self.add(first, last)), best)
        return best


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
