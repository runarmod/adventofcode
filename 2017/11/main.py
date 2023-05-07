class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = open(filename).read().rstrip().split(",")

    def distance(self, x, y):
        distance = 0
        x, y = abs(x), abs(y)
        tmp_x = tmp_y = 0
        while tmp_x < x:
            tmp_x += 1
            tmp_y += 1
            distance += 1
        while tmp_y < y:
            tmp_y += 2
            distance += 1
        return distance

    def part1(self):
        x = 0
        y = 0

        # x positive to right, y positive up
        self.max_distance = 0
        for dir in self.data:
            match dir:
                case "n":
                    y += 2
                case "s":
                    y -= 2
                case "ne":
                    x += 1
                    y += 1
                case "se":
                    x += 1
                    y -= 1
                case "nw":
                    x -= 1
                    y += 1
                case "sw":
                    x -= 1
                    y -= 1
            self.max_distance = max(self.max_distance, self.distance(x, y))
        return self.distance(x, y)

    def part2(self):
        return self.max_distance


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
