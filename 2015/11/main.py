import string
import re


class Solution():
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.password = open(filename).read().rstrip()
        self.alphabet = string.ascii_lowercase
        self.hasToInclude = [self.alphabet[i:i+3]
                             for i in range(len(self.alphabet) - 2)]

    def passwordIsAllowed(self):
        # Rule 1
        if all(s not in self.password for s in self.hasToInclude):
            return False

        # Rule 2
        if re.findall(r"[iol]", self.password):
            return False

        # Rule 3
        if not re.findall(r'.*(.)\1.*(.)\2.*', self.password):
            return False

        return True

    def incrementPassword(self):
        for i in range(len(self.password) - 1, -1, -1):
            if self.password[i] == self.alphabet[-1]:
                self.password = self.password[:i] + \
                    self.alphabet[0] + self.password[i+1:]
            else:
                self.password = self.password[:i] + \
                    chr(ord(self.password[i]) + 1) + self.password[i+1:]
                break
        return self.password

    def part1(self):
        while not self.passwordIsAllowed():
            self.incrementPassword()
        return self.password

    def part2(self):
        self.incrementPassword()
        return self.part1()


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
