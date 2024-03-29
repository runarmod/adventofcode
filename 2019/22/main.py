import re
import time

from sympy import isprime


def parse_line(line):
    m = re.match(
        r"(cut|deal with increment|deal into new stack) ?(-?\d+)?", line
    ).groups()
    if m[1]:
        return m[0], int(m[1])
    return (m[0],)


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.lines = list(map(parse_line, open(filename).read().rstrip().split("\n")))

    def deal_into_new_stack_index(self, c):
        return (-c - 1) % self.card_count

    def cut_index(self, c, n):
        return (c - n) % self.card_count

    def deal_with_increment_index(self, c, n):
        return (c * n) % self.card_count

    def part1(self):
        self.card_count = 10 if self.test else 10007

        card_index = 0 if self.test else 2019
        for line in self.lines:
            match line:
                case ("deal into new stack",):
                    card_index = self.deal_into_new_stack_index(card_index)
                case ("cut", n):
                    card_index = self.cut_index(card_index, n)
                case ("deal with increment", n):
                    card_index = self.deal_with_increment_index(card_index, n)
        return card_index

    def part2(self):
        self.card_count = 119315717514047

        assert isprime(
            self.card_count
        ), "The card count has to be prime to use Fermat's Little Theorem."

        tot_mul, tot_add = 1, 0
        for line in self.lines:
            mul, add = 1, 0
            match line:
                case ("deal into new stack",):
                    mul = add = -1
                case ("cut", n):
                    mul, add = 1, -n
                case ("deal with increment", n):
                    mul, add = n, 0
            tot_mul = (tot_mul * mul) % self.card_count
            tot_add = (tot_add * mul + add) % self.card_count

        M = 101741582076661
        fin_mul = pow(tot_mul, M, self.card_count)
        # fin_add = ... + tot_mul ** 3 * tot_add + tot_mul ** 2 * tot_add + tot_mul ** 1 * tot_add + tot_mul ** 0 * tot_add
        # = tot_add * (1 + tot_mul + tot_mul ** 2 + tot_mul ** 3 + ... + tot_mul ** (M - 1))
        # = tot_add * (tot_mul ** M - 1) / (tot_mul - 1) (as per geometric series formula)
        # = tot_add * (tot_mul ** M - 1) * pow(tot_mul - 1, -1, self.cardCount) (as per Fermat's Little Theorem)
        # = tot_add * (fin_mul - 1) * pow(tot_mul - 1, -1, self.cardCount)
        fin_add = (
            tot_add * (fin_mul - 1) * pow(tot_mul - 1, -1, self.card_count)
        ) % self.card_count

        target_card = 2020
        # (fin_mul * target_card + fin_add) % self.cardCount = position
        # fin_mul * target_card + fin_add = position + k * self.cardCount
        # target_card  = (position - fin_add + k * self.cardCount) / fin_mul
        # target_card  = (position - fin_add + k * self.cardCount) * fin_mul**(-1)
        # target_card = ((position - fin_add) * pow(fin_mul, -1, self.cardCount)) % self.cardCount
        return (
            (target_card - fin_add) * pow(fin_mul, -1, self.card_count)
        ) % self.card_count


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 7 else 'wrong :('}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
