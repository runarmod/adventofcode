import itertools
import time
import numpy as np


def parseMap(_map):
    return [list(line) for line in _map.split("\n")]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            parseMap(line) for line in open(filename).read().rstrip().split("\n\n")
        ]

    def find_horizontal_reflection(self, _map):
        return self.find_vertical_reflection(np.array(_map).transpose().tolist())

    def find_vertical_reflection(self, _map):
        out = []
        for y in range(len(_map) - 1):
            for left, right in zip(_map[y::-1], _map[y + 1 :]):
                if left != right:
                    break
            else:
                out.append(y + 1)
        return out

    def part1(self):
        s = 0
        for _map in self.data:
            if ver := self.find_vertical_reflection(_map):
                s += 100 * ver[0]
            elif hor := self.find_horizontal_reflection(_map):
                s += hor[0]
        return s

    def part2(self):
        s = 0
        for _map in self.data:
            if orginal_ver := self.find_vertical_reflection(_map):
                orginal_ver = orginal_ver[0]

            if orginal_hor := self.find_horizontal_reflection(_map):
                orginal_hor = orginal_hor[0]

            for x, y in itertools.product(range(len(_map[0])), range(len(_map))):
                new_map = [line[:] for line in _map]
                new_map[y][x] = "#" if new_map[y][x] == "." else "."

                if ver := [
                    v
                    for v in self.find_vertical_reflection(new_map)
                    if v != orginal_ver
                ]:
                    s += 100 * ver[0]
                    break

                if hor := [
                    v
                    for v in self.find_horizontal_reflection(new_map)
                    if v != orginal_hor
                ]:
                    s += hor[0]
                    break
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 405 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 400 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
