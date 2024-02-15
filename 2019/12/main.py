import itertools
import math
import re
import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.steps = 100 if self.test else 1000
        self.pos = [
            list(map(int, re.findall(r"-?\d+", line)))
            for line in open(filename).read().rstrip().split("\n")
        ]
        self.speeds = [[0, 0, 0] for _ in range(len(self.pos))]

        self.run()

    def total_energy(self, pos, vel):
        s = 0
        for moon in range(len(pos)):
            s += sum(abs(x) for x in pos[moon]) * sum(abs(x) for x in vel[moon])
        return s

    def tuplify(self, l1, l2, coord_idx):
        return (tuple(x[coord_idx] for x in l1), tuple(x[coord_idx] for x in l2))

    def run(self):
        loops = 1

        part1_pos = [[0, 0, 0] for _ in range(len(self.pos))]
        part1_speed = [[0, 0, 0] for _ in range(len(self.speeds))]
        for c_i in range(3):
            d = set()
            for i in itertools.count():
                if i == self.steps:
                    for m_i in range(len(self.pos)):
                        part1_pos[m_i][c_i] = self.pos[m_i][c_i]
                        part1_speed[m_i][c_i] = self.speeds[m_i][c_i]

                for moon1, moon2 in itertools.permutations(range(len(self.speeds)), 2):
                    diff = self.pos[moon1][c_i] - self.pos[moon2][c_i]

                    if diff < 0:
                        self.speeds[moon1][c_i] += 1
                    elif diff > 0:
                        self.speeds[moon1][c_i] -= 1

                for m_i in range(len(self.pos)):
                    self.pos[m_i][c_i] += self.speeds[m_i][c_i]

                t = self.tuplify(self.pos, self.speeds, c_i)
                if t in d:
                    loops = math.lcm(loops, i)
                    break
                d.add(t)
        self.energy = self.total_energy(part1_pos, part1_speed)
        self.loops = loops

    def part1(self):
        return self.energy

    def part2(self):
        return self.loops


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1},\t\t{'correct :)' if test1 == 1940 else 'wrong :('}")
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 4686774924 else 'wrong :('}"
    )

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
