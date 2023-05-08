from itertools import count


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = tuple(
            map(
                lambda line: (tuple(map(int, line.split(": ")))),
                open(filename).read().rstrip().split("\n"),
            )
        )

    def collision(self, delay=0) -> bool:
        return any((k + delay) % ((v - 1) * 2) == 0 for k, v in self.data)

    def collision_score(self) -> int:
        return sum(k * v for k, v in self.data if k % ((v - 1) * 2) == 0)

    def part1(self):
        return self.collision_score()

    def part2(self):
        return next(i for i in count(step=2) if not self.collision(i))


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
