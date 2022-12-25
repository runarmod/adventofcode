class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(open(filename).read().rstrip().split("\n"))
        self.n_to_s = {
            "-2": "=",
            "-1": "-",
            "0": "0",
            "1": "1",
            "2": "2",
        }
        self.s_to_n = {v: k for k, v in self.n_to_s.items()}

    def digit_to_snafu(self, n):
        return self.n_to_s[str(n)]

    def snafu_to_digit(self, s):
        return int(self.s_to_n[s])

    def to_int(self, s):
        return sum(
            self.snafu_to_digit(s[i]) * 5**e
            for e, i in enumerate(range(len(s) - 1, -1, -1))
        )

    def to_snafu(self, n):
        digits = []
        while n:
            n, r = divmod(n, 5)
            digits.append(r)
        for i in range(len(digits)):
            if digits[i] > 2:
                digits[i] -= 5
                if i == len(digits) - 1:
                    digits.append(1)
                else:
                    digits[i + 1] += 1
        return "".join(self.digit_to_snafu(d) for d in digits[::-1])

    def part1(self):
        return self.to_snafu(sum(self.to_int(s) for s in self.data))


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")


if __name__ == "__main__":
    main()
