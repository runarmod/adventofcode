import functools
import itertools
import time
from collections import deque
from tqdm import tqdm


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [list(line) for line in open(filename).read().rstrip().split("\n")]
        self.open = {
            (x, y)
            for x, y in itertools.product(
                range(len(self.data)), range(len(self.data[0]))
            )
            if self.data[x][y] in ".S"
        }
        self.start = next(
            (x, y)
            for x, y in itertools.product(
                range(len(self.data)), range(len(self.data[0]))
            )
            if self.data[x][y] == "S"
        )

        self.COUNT = 5_001 if self.test else 26_501_365

        self.ROWS = len(self.data)
        self.COLS = len(self.data[0])

    def part1(self):
        q = deque()
        q.append(self.start)
        for _ in range(6 if self.test else 64):
            new_q = deque()
            v = set()
            while q:
                x, y = q.popleft()
                for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    if (x + dx, y + dy) in self.open:
                        if (x + dx, y + dy) not in v:
                            new_q.append((x + dx, y + dy))
                            v.add((x + dx, y + dy))
            q = new_q
        # self.print(q)
        return len(q)

    def print(self, q):
        for x, y in q:
            self.data[x][y] = "O"
        print("\n".join("".join(row) for row in self.data))
        print()

    def get_distances(self):
        ROWS = len(self.data)
        COLS = len(self.data[0])
        distances = {}
        q = deque()
        q.append((*self.start, 0, 0, 0))  # x, y, grid_x, grid_y, distance
        while q:
            x, y, gx, gy, distance = q.popleft()
            gx -= x < 0
            gx += x >= COLS
            gy -= y < 0
            gy += y >= ROWS

            x %= COLS
            y %= ROWS

            if (x, y, gx, gy) in distances:
                continue
            if (x, y) not in self.open:
                continue

            if abs(gx) > 3 or abs(gy) > 3:
                continue

            distances[(x, y, gx, gy)] = distance
            for dx, dy in {(0, 1), (1, 0), (-1, 0), (0, -1)}:
                q.append((x + dx, y + dy, gx, gy, distance + 1))
        return distances

    @functools.lru_cache(None)
    def get_count(self, distance, corner):
        grid_extra = (self.COUNT - distance) // self.ROWS
        ans = 0

        """
        Some optimazations used here:

        Want to add the number of positions where distance plus multiples of ROWS is same
        parity as COUNT. Since ROWS is odd, then the new distance is odd only if distance
        and the multiple are opposite parity. Therefore I use the fact that len of a range
        is O(1), and I either start at 1 or 2 depending on the parity of distance.

        If we are at a corner however, we also want to add the count of outgoing lengths.
        Here this is done by using the arithmetic series formula.
        """
        start = 1 if distance % 2 == 0 else 2
        if corner:
            # Arithmetic series
            length = len(range(start, grid_extra + 1, 2))
            ans += length * ((start + grid_extra) // 2)
        ans += len(range(start, grid_extra + 1, 2))
        return ans

    def part2(self):
        distances = self.get_distances()
        assert (
            self.ROWS == self.COLS
        ), f"Multiple optimizations used are not possible if ROWS != COLS"
        assert (
            self.ROWS % 2 == 1
        ), f"Multiple optimizations used are not possible if ROWS(/COLS) is even"
        assert (
            self.COUNT % 2 == 1
        ), f"An optimization used (in function get_count) is not possible if COUNT is even"

        ans = 0
        for x, y in tqdm(
            itertools.product(range(self.COLS), range(self.ROWS)),
            total=self.COLS * self.ROWS,
        ):
            if (x, y, 0, 0) not in distances:
                continue
            for gx, gy in itertools.product(range(-3, 4), repeat=2):
                distance = distances[(x, y, gx, gy)]
                assert distance <= self.COUNT
                if distance % 2 == self.COUNT % 2:
                    ans += 1
                if abs(gx) == 3 and abs(gy) == 3:
                    ans += self.get_count(distance, True)
                elif abs(gx) == 3 or abs(gy) == 3:
                    ans += self.get_count(distance, False)
        return ans


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1},\t\t{'correct :)' if test1 == 16 else 'wrong :('}")
    print(
        f"(TEST) Part 2: {test2},\t{'correct :)' if test2 == 16739403 else 'wrong :('}"
    )

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    assert part1 == 3814
    assert part2 == 632257949158206


if __name__ == "__main__":
    main()
