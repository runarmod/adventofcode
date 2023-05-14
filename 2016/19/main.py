from collections import deque


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.elves = int(open(filename).read().strip())
        self.giftless = set()

    def part1(self):
        q = deque(range(1, self.elves + 1))
        while len(q) > 1:
            q.rotate(-1)
            q.popleft()
        return q.popleft()

    def part2(self):
        # Full list = left + right (left[-1] and right[0] are the middle)
        left = deque(range(1, self.elves // 2 + 1))
        right = deque(range(self.elves // 2 + 1, self.elves + 1))

        while left and right:
            if len(left) > len(right):
                left.pop()
            else:
                right.popleft()

            # Full list .rotate(-1)
            right.append(left.popleft())
            left.append(right.popleft())
        return left[0]


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
