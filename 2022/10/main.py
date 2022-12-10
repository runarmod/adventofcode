import re


def parseLine(line):
    line = list(re.findall(r"(noop|addx) ?(-?\d+)?", line)[0])
    if line[0] == "noop":
        line[1] = 0
    return line[0], int(line[1])


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseLine(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        def update_signal():
            nonlocal cycle_nr, X, signal
            if cycle_nr == 20 or (cycle_nr - 20) % 40 == 0:
                signal += cycle_nr * X

        X = 1
        cycle_nr = 1
        signal = 0
        for line in self.data:
            update_signal()
            if line[0] == "addx":
                cycle_nr += 1
                update_signal()
                X += line[1]
            cycle_nr += 1
        return signal

    def part2(self):
        def update_pixels():
            nonlocal cycle_nr, X, pixels
            if abs(X - cycle_nr % 40) < 2:
                pixels[cycle_nr // 40][cycle_nr % 40] = "#"

        X = 1
        cycle_nr = 0

        pixels = [[" " for _ in range(40)] for _ in range(6)]
        for line in self.data:
            update_pixels()
            if line[0] == "addx":
                cycle_nr += 1
                update_pixels()
                X += line[1]
            cycle_nr += 1
        self.render(pixels)

    def render(self, pixels):
        for line in pixels:
            print("".join(line))


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print("(TEST) Part 2:")
    test.part2()

    solution = Solution()
    part1 = solution.part1()
    part2 = "ZRARLFZU"
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")
    solution.part2()

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


if __name__ == "__main__":
    main()
