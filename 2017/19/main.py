import itertools


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = [list(line) for line in open(filename).read().split("\n")[:-1]]

    def get_start(self):
        for y, x in itertools.product(range(len(self.data)), range(len(self.data[0]))):
            if self.data[y][x] != " ":
                return x, y

    def get_new_direction(self, x, y, direction):
        # Remove the same direction, and the opposite direction
        directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}.difference(
            {direction, tuple(map(lambda x: -x, direction))}
        )
        for _dir in directions:
            new_x, new_y = x + _dir[0], y + _dir[1]
            if not (0 <= new_x < len(self.data[0]) and 0 <= new_y < len(self.data)):
                continue
            if self.data[new_y][new_x] != " ":
                return _dir

    def part1(self):
        x, y = self.get_start()
        direction = (0, 1)
        letters = ""
        steps = 0
        while 0 <= x < len(self.data[0]) and 0 <= y < len(self.data):
            x, y = x + direction[0], y + direction[1]
            steps += 1
            value = self.data[y][x]
            if value == " ":
                self.steps = steps
                return letters
            if value.isalpha():
                letters += value
                continue
            if value == "+":
                direction = self.get_new_direction(x, y, direction)
        return None

    def part2(self):
        return self.steps


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
