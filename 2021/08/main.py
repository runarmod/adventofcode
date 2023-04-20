def parse(line):
    return [part.split(" ") for part in line.split(" | ")]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parse(line) for line in open(filename).read().rstrip().split("\n")]
        self.digs_length = {2: 1, 5: [2, 3, 5], 4: 4, 6: [6, 9, 0], 3: 7, 7: 8}

    def part1(self):
        s = 0
        for line in self.data:
            for num in line[1]:
                if len(num) in {2, 4, 3, 7}:
                    s += 1
        return s

    def part2(self):
        _sum = 0

        for line in self.data:
            part1 = set(line[0])
            self.numbers = [None for _ in range(10)]

            # Find 1, 4, 7, 8
            self.generate_easy_parts(part1)

            # Find 6 and 9 and 0
            self.find_6_9_0(part1)

            # Find 2 and 3 and 5
            self.find_2_3_5(part1)

            output = ""
            for letters_string in line[1]:
                letters = set(letters_string)
                output += str(self.numbers.index(letters))
            _sum += int(output)
        return _sum

    def find_6_9_0(self, part1):
        for num in part1:
            if len(num) != 6:
                continue
            num = set(num)

            if len(self.numbers[1] - num) == 1:
                self.numbers[6] = num
                continue

            if len(num - self.numbers[4]) == 2:
                self.numbers[9] = num
                continue
            if len(num - self.numbers[4]) == 3:
                self.numbers[0] = num
                continue
            print("ERROR 6, 9, 0")

    def find_2_3_5(self, part1):
        for num in part1:
            if len(num) != 5:
                continue
            num = set(num)

            if len(num - self.numbers[1]) == 3:
                self.numbers[3] = num
                continue
            if len(num - self.numbers[6]) == 0:
                self.numbers[5] = num
                continue
            if len(num - self.numbers[6]) == 1:
                self.numbers[2] = num
                continue
            print("ERROR 2, 3, 5")

    def generate_easy_parts(self, line):
        for part in line:
            if len(part) == 2:
                self.numbers[1] = set(part)
            elif len(part) == 3:
                self.numbers[7] = set(part)
            elif len(part) == 4:
                self.numbers[4] = set(part)
            elif len(part) == 7:
                self.numbers[8] = set(part)


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
