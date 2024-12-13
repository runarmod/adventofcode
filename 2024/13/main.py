import re
import time

from aoc_utils_runarmod import get_data
from sympy import Eq, diophantine, solve, symbols
from sympy.abc import a, b


def parseNumbers(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 13) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n\n")
        )

        self.data = []
        for section in data:
            s = []
            for line in section.split("\n"):
                s.append(parseNumbers(line))
            self.data.append(s)

    def solve(self, A, B, prize):
        eq1 = Eq(A[0] * a + B[0] * b, prize[0])
        eq2 = Eq(A[1] * a + B[1] * b, prize[1])

        sol = diophantine(eq1)
        if not sol:
            return 0
        solutions_eq1 = next(iter(sol))

        a_sol, b_sol = solutions_eq1

        eq2_sub = eq2.subs({a: a_sol, b: b_sol})
        t_values = solve(eq2_sub)
        if not t_values:
            return 0

        t_0 = symbols("t_0", integer=True)
        final_solutions = [
            (a_sol.subs(t_0, t_val), b_sol.subs(t_0, t_val)) for t_val in t_values
        ]
        assert len(final_solutions) == 1

        countA, countB = final_solutions[0]
        return countA * 3 + countB

    def run(self, prize_func=lambda x: x):
        s = 0
        for machine in self.data:
            A, B, prize = machine
            s += self.solve(A, B, list(map(prize_func, prize)))
        return s

    def part1(self):
        return self.run()

    def part2(self):
        return self.run(prize_func=lambda x: x + 10**13)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 480 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
