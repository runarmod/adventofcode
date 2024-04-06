class Solution:
    def __init__(self, test=False):
        self.test = test
        self.row = 2981
        self.col = 3075

    def part1(self):
        val = 20151125
        x = y = maxx = 1
        for _ in range(1000000000000):
            if y <= 1:
                maxx += 1
                y = maxx
                x = 1
            else:
                x += 1
                y -= 1
            val = (val * 252533) % 33554393
            if y == self.row and x == self.col:
                return val

    def part2(self):
        return None


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
