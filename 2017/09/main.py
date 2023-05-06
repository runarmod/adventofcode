def parseLine(line):
    return line


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.string = open(filename).read().rstrip()

    def find_opening_index(self, index):
        ignore = False
        waste = False
        for i in range(index, len(self.string)):
            if self.string[i - 1] != "!":
                ignore = False
            if self.string[i] == "!":
                ignore = not ignore
                continue
            if self.string[i] == "<" and not ignore:
                waste = True
                continue
            if self.string[i] == ">" and not ignore:
                waste = False
                continue
            if self.string[i] == "{" and not waste and not ignore:
                return i
        return None

    def find_closing_index(self, index):
        ignore = False
        waste = False
        count = 0
        for i in range(index + 1, len(self.string)):
            if self.string[i - 1] != "!":
                ignore = False
            if self.string[i] == "!":
                ignore = not ignore
                continue
            if self.string[i] == "<" and not ignore:
                waste = True
                continue
            if self.string[i] == ">" and not ignore:
                waste = False
                continue
            if self.string[i] == "{" and not waste and not ignore:
                count += 1
                continue
            if self.string[i] == "}" and not waste and not ignore:
                if count == 0:
                    return i
                count -= 1
        return None

    def part1(self):
        i = 0
        groups = []
        while i < len(self.string):
            start = self.find_opening_index(i)
            if start is None:
                break
            end = self.find_closing_index(start)
            groups.append((start, end))
            i = start + 1
        depths = {}
        for start, end in groups:
            depths[(start, end)] = next(
                (
                    tmpdepth + 1
                    for (tmpstart, tmpend), tmpdepth in sorted(
                        list(depths.items()), key=lambda x: x[0][0], reverse=True
                    )
                    if tmpstart < start < end < tmpend
                ),
                1,
            )
        return sum(depths.values())

    def part2(self):
        ignore = False
        waste = False
        count = 0
        for i in range(len(self.string)):
            if self.string[i - 1] != "!":
                ignore = False
            if self.string[i] == "!":
                ignore = not ignore
                continue
            if self.string[i] == "<" and not ignore:
                if waste:
                    count += 1
                else:
                    waste = True
                continue
            if self.string[i] == ">" and not ignore:
                if waste:
                    waste = False
                else:
                    count += 1
                continue
            if waste and not ignore:
                count += 1
        return count


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
