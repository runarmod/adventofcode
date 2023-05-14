import re


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = open(filename).read().rstrip().split("\n")
        self.start_word1 = "abcde" if test else "abcdefgh"
        self.start_word2 = "fbgdceah"

        self.instructions = [
            (r"swap position (\d+) with position (\d+)", self.swap, self.swap),
            (r"swap letter (\w) with letter (\w)", self.swap, self.swap),
            (r"rotate (left|right) (\d+) step", self.rotate_steps, self.rotate_steps_alt),
            (r"rotate based on position of letter (\w)", self.rot_letter, self.rot_letter_alt),
            (r"reverse positions (\d+) through (\d+)", self.reverse, self.reverse),
            (r"move position (\d+) to position (\d+)", self.move, self.move_alt),
        ]

    def swap(self, word, info1, info2):
        tmp = word[:]
        if info1.isalpha():
            i, j = tmp.index(info1), tmp.index(info2)
        else:
            i, j = int(info1), int(info2)
        tmp[i], tmp[j] = tmp[j], tmp[i]
        return tmp

    def rotate_steps(self, word, direction, steps):
        steps = int(steps)
        steps %= len(word)
        if direction == "right":
            steps *= -1
        return word[steps:] + word[:steps]

    def rotate_steps_alt(self, word, direction, steps):
        return self.rotate_steps(word, direction, -int(steps))

    def rotate(self, word: list[str], distance: int):
        distance %= len(word)
        return word[-distance:] + word[:-distance]

    def rot_letter(self, word, letter):
        index = word.index(letter)
        word = self.rotate(word, 1 + index + (1 if index >= 4 else 0))
        return word

    def rot_letter_alt(self, word, letter):
        for i in range(len(word) + 2):
            new = self.rotate_steps(word, "right", i)
            rotated = self.rot_letter(new, letter)
            if rotated == word:
                return new

    def reverse(self, word, i, j):
        i, j = int(i), int(j)
        word = word[:i] + word[i : j + 1][::-1] + word[j + 1 :]
        return word

    def move(self, word, i, j):
        tmp = word[:]
        idx = tmp[int(i)]
        tmp.remove(idx)
        tmp.insert(int(j), idx)
        return tmp

    def move_alt(self, word, i, j):
        return self.move(word, j, i)

    def part1(self):
        word = list(self.start_word1)
        for line in self.data:
            for instruction, func, _ in self.instructions:
                if match := re.match(instruction, line):
                    word = func(word, *match.groups())
                    break
        return "".join(word)

    def part2(self):
        word = list(self.start_word2)
        for line in self.data[::-1]:
            for instruction, _, alt_func in self.instructions:
                if match := re.match(instruction, line):
                    word = alt_func(word, *match.groups())
                    break
        return "".join(word)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
