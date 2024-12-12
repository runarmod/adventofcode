import time
from collections import deque

from aoc_utils_runarmod import get_data


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            (get_data(2024, 12) if not self.test else open("testinput.txt").read())
            .rstrip()
            .split("\n")
        )
        self.data = data

    def get_regions(self):
        visited = set()
        regions = []
        for y, line in enumerate(self.data):
            for x, letter in enumerate(line):
                if (x, y) in visited:
                    continue
                region = set()
                q = deque([(x, y)])
                while q:
                    curr_x, curr_y = q.popleft()
                    if (curr_x, curr_y) in region:
                        continue
                    region.add((curr_x, curr_y))
                    visited.add((curr_x, curr_y))
                    for new_x, new_y in neighbors4((curr_x, curr_y)):
                        if (
                            new_y in range(len(self.data))
                            and new_x in range(len(line))
                            and self.data[new_y][new_x] == letter
                        ):
                            q.append((new_x, new_y))
                regions.append(region)
        return regions

    def area(self, region: set):
        return len(region)

    def perimeter(self, region: set, part: int):
        perim = []
        for x, y in region:
            curr_perim = set()
            for new_x, new_y in neighbors4((x, y)):
                if not (
                    new_y in range(len(self.data))
                    and new_x in range(len(self.data[new_y]))
                    and (new_x, new_y) in region
                ):
                    curr_perim.add((new_x, new_y, x - new_x, y - new_y))
            perim.extend(curr_perim)
        if part == 1:
            return len(perim)

        # Walk along the fence the same direction as this fence stands.
        # Only add 1 per fence-section.
        # We have to keep track of the direction "this" x and y refer to,
        # i.e. which direction the inside of the region is, since one x,y coord can
        # have two (or even 3-4) fences (each ment for their own side).
        ans = 0
        seen = set()
        for x, y, dir_inside_x, dir_inside_y in perim:
            if (x, y, dir_inside_x, dir_inside_y) in seen:
                continue
            ans += 1
            seen.add((x, y, dir_inside_x, dir_inside_y))
            new_x, new_y = x, y
            while (new_x, new_y, dir_inside_x, dir_inside_y) in perim:
                seen.add((new_x, new_y, dir_inside_x, dir_inside_y))
                new_x += dir_inside_y
                new_y += dir_inside_x
            new_x, new_y = x, y
            while (new_x, new_y, dir_inside_x, dir_inside_y) in perim:
                seen.add((new_x, new_y, dir_inside_x, dir_inside_y))
                new_x -= dir_inside_y
                new_y -= dir_inside_x
        return ans

    def run(self, part: int):
        return sum(
            self.area(region) * self.perimeter(region, part=part)
            for region in self.get_regions()
        )

    def part1(self):
        return self.run(part=1)

    def part2(self):
        return self.run(part=2)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 1930 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 1206 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield point[:i] + (point[i] + diff,) + point[i + 1 :]


if __name__ == "__main__":
    main()
