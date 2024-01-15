import re
import time
from typing import Callable
import z3

"""
I NEED INFO ON THESE LINES (indexes): 4, 5, 15
SOLVE FOR INDEX 0

Line-numbers:
    0           1          2          3          4          5          6          7          8          9          10         11         12         13         14         15         16         17
     w = ?      x = 0      x = z      x %= 26    z //= ?    x += ?    x = x==w   x = x==0    y = 0      y = 25     y *= x     y += 1     z *= y     y = 0      y += w     y += ?     y *= x     z += y
                                                                            x = x!=w                      if x==w: (y = 0) (y = y)
                                                                           ^      ^                                  ^
[
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y',
    'inp w      mul x 0    add x z    mod x 26   div z ??   add x ???  eql x w    eql x 0    mul y 0    add y 25   mul y x    add y 1    mul z y    mul y 0    add y w    add y ??   mul y x    add z y'
 ]
 """


class Solution:
    def __init__(self):
        self.data = re.findall(r"(\w+) (\w+) ?(-?\w+|\d+)?", open("input.txt").read())
        self.SECTIONS = 14
        self.SECTION_LENGTH = 18

    def get_values(self):
        div, plus, plus2 = [], [], []
        div_sub_line = 4
        plus_sub_line = 5
        plus2_sub_line = 15

        for section_number in range(self.SECTIONS):
            section_line = section_number * self.SECTION_LENGTH
            div.append(int(self.data[section_line + div_sub_line][2]))
            plus.append(int(self.data[section_line + plus_sub_line][2]))
            plus2.append(int(self.data[section_line + plus2_sub_line][2]))
        return div, plus, plus2

    def run(self, operator: Callable[[int, int], bool]):
        """
        There are 14 sections with 18 lines per section. Each section is organized like this:

        ```py
        z //= (index 4 (called DIV))
        x = z % 26 + (index 5 (called PLUS))
        if x != w:
            z = 26 * z + w + (index 15 (called PLUS2))
        ```
        """

        # First create the statement that we want to solve
        solver = z3.Solver()
        ws = [z3.Int(f"w{i}") for i in range(self.SECTIONS)]
        for w in ws:
            solver.add(z3.And(w >= 1, w <= 9))
        answer = sum(ws[i] * 10 ** (13 - i) for i in range(len(ws)))

        z = z3.Int("z")
        DIV, PLUS, PLUS2 = self.get_values()
        for i in range(self.SECTIONS):
            x = z % 26
            z /= DIV[i]
            z += z3.If(x + PLUS[i] != ws[i], 25 * z + ws[i] + PLUS2[i], 0)

        # z should finally be 0
        solver.add(z == 0)

        # Now solve the statement for the largest/smallest solution
        best = None
        while solver.check() == z3.sat:
            best = solver.model().eval(answer).as_long()
            solver.add(operator(answer, best))

        return best

    def part1(self):
        return self.run(lambda a, b: a > b)

    def part2(self):
        return self.run(lambda a, b: a < b)


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
