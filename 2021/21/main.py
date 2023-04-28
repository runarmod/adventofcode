import functools
import itertools
import re


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.START_POS = [
            int(re.findall(r": (\d+)", line)[0])
            for line in open(filename).read().rstrip().split("\n")
        ]

        self.dice = 0

    def roll_dice_part_1(self):
        self.dice = (self.dice % 100) + 1
        return self.dice

    def get_new_position(self, position, moves):
        p = position - 1
        p += moves
        p %= 10
        p += 1
        return p

    def part1(self):
        pos = list(self.START_POS)
        scores = [0, 0]
        rounds = -1
        while True:
            rounds += 1
            score = self.get_new_position(
                pos[rounds % 2], sum(self.roll_dice_part_1() for _ in range(3))
            )
            scores[rounds % 2] += score
            pos[rounds % 2] = score
            if scores[rounds % 2] >= 1000:
                return scores[(rounds + 1) % 2] * (rounds + 1) * 3

    @functools.lru_cache(maxsize=None)
    def play_out(self, p1, s1, p2, s2):
        wins1 = wins2 = 0
        for dice_value in itertools.product((1, 2, 3), repeat=3):
            new_p1 = sum((p1, *dice_value, -1)) % 10 + 1
            new_s1 = s1 + new_p1
            if new_s1 >= 21:
                wins1 += 1
            else:
                w2_copy, w1_copy = self.play_out(p2, s2, new_p1, new_s1)
                wins1 += w1_copy
                wins2 += w2_copy
        return wins1, wins2

    def part2(self):
        return max(self.play_out(self.START_POS[0], 0, self.START_POS[1], 0))


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
