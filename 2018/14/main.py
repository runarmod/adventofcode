import time


class Chef:
    def __init__(self, *start_values):
        if len(start_values) < 2:
            raise ValueError("Has to start with at least two values")
        self.recipies = [*start_values]
        self.i, self.j = 0, 1

    def __next__(self):
        add = self.recipies[self.i] + self.recipies[self.j]
        self.recipies.extend(divmod(add, 10) if add >= 10 else (add,))
        self.i = (self.i + self.recipies[self.i] + 1) % len(self.recipies)
        self.j = (self.j + self.recipies[self.j] + 1) % len(self.recipies)

    def __len__(self) -> int:
        return len(self.recipies)

    def get_score(self, start_index, length=0):
        if length == 0:
            length = len(self.recipies) - start_index + 1
        return "".join(map(str, self.recipies[start_index : start_index + length]))

    def find(self, score):
        if self.get_score(-len(score), len(score)) == score:
            return len(self.recipies) - len(score)
        if self.get_score(-len(score) - 1, len(score)) == score:
            return len(self.recipies) - len(score) - 1
        return 0


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.score_str = open(filename).read().rstrip()
        self.recipies_count = int(self.score_str)

    def part1(self):
        recipies = Chef(3, 7)
        while len(recipies) < self.recipies_count + 10:
            next(recipies)
        return recipies.get_score(self.recipies_count, 10)

    def part2(self):
        recipies = Chef(3, 7)
        while True:
            next(recipies)
            if index := recipies.find(self.score_str):
                return index


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
