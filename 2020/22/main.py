from collections import deque
from itertools import islice
import re
import time


def parsePlayer(lines):
    return list(map(int, re.findall(r"\d+", lines)[1:]))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parsePlayer(line) for line in open(filename).read().rstrip().split("\n\n")
        ]

    def part1(self):
        p1, p2 = map(deque, self.data)

        while len(p1) > 0 and len(p2) > 0:
            if p1[0] > p2[0]:
                p1.rotate(-1)
                p1.append(p2.popleft())
            else:
                p2.rotate(-1)
                p2.append(p1.popleft())

        return (
            lambda player: sum(
                (len(player) - i) * player[i] for i in range(len(player))
            )
        )(p1 if len(p1) > 0 else p2)

    def part2(self):
        def play(p1: deque[int], p2: deque[int]) -> tuple[bool, deque[int]]:
            cache = set()

            while len(p1) > 0 and len(p2) > 0:
                if tuple(p1) in cache:
                    return True, max([p1, p2], key=len)
                cache.add(tuple(p1))

                p1card, p2card = p1.popleft(), p2.popleft()

                winnerIsPlayer1 = p1card > p2card
                if len(p1) >= p1card and len(p2) >= p2card:
                    winnerIsPlayer1, _ = play(
                        *(
                            deque(islice(p, 0, pcard))
                            for p, pcard in ((p1, p1card), (p2, p2card))
                        )
                    )

                if winnerIsPlayer1:
                    p1.append(p1card)
                    p1.append(p2card)
                else:
                    p2.append(p2card)
                    p2.append(p1card)
            return winnerIsPlayer1, max([p1, p2], key=len)

        _, winner = play(*map(deque, self.data))

        return sum((len(winner) - i) * winner[i] for i in range(len(winner)))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 306 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 291 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
