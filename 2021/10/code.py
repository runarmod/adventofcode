from collections import deque


class Solution():
    def __init__(self, test=False):
        file = "testinput.txt" if test else "input.txt"
        self.data = open(file).read().rstrip().split("\n")
        self.first_corrupts = []
        self.bracket_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
        self.wrong_total_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
        self.wrong_total_score = 0
        self.missing_scores = {")": 1, "]": 2, "}": 3, ">": 4}
        self.missing_total_score = 0
        self.missing_points = []

    def get_first_corrupt(self, line):
        queue = deque()
        queue.append(None)
        for c in line:
            if c in self.bracket_pairs:
                queue.append(self.bracket_pairs[c])
            else:
                popped = queue.pop()
                if popped is None or popped != c:
                    return c
        return None

    def get_missing_brackets(self, line):
        queue = deque()
        queue.append(None)
        res = ""
        for c in line:
            if c in self.bracket_pairs:
                queue.append(self.bracket_pairs[c])
            else:
                popped = queue.pop()
                if popped is None or popped != c:
                    return ""
        while b := queue.pop():
            res += b
        return res

    def save_first_corrupts(self):
        for line in self.data:
            if corrupt := self.get_first_corrupt(line):
                self.first_corrupts.append(corrupt)

    def get_wrong_score(self, c):
        return self.wrong_total_scores[c]

    def calculate_score_wrong(self):
        for corrupt in self.first_corrupts:
            self.wrong_total_score += self.get_wrong_score(corrupt)

    def calculate_line_score_missing(self, line):
        score = 0

        missing = self.get_missing_brackets(line)
        for c in missing:
            score *= 5
            score += self.missing_scores[c]

        return score

    def part1(self):
        self.save_first_corrupts()
        self.calculate_score_wrong()
        return self.wrong_total_score

    def part2(self):
        self.missing_points = [s for s in [
            self.calculate_line_score_missing(line) for line in self.data] if s != 0]
        self.missing_points.sort()
        return self.missing_points[len(self.missing_points) // 2]


def main():
    solution = Solution(test=False)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
