from collections import Counter, deque
import itertools
import numpy as np
import scipy
import time


def parse_scanner(section: str) -> list[tuple[int, int, int]]:
    lines = section.split("\n")
    return [tuple(map(int, line.split(","))) for line in lines[1:]]


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = (
            parse_scanner(section)
            for section in open(filename).read().rstrip().split("\n\n")
        )
        self.scanner_coords = {((0, 0, 0))}

    def all_rotations(
        self, points: list[int, int, int]
    ) -> list[list[tuple[int, int, int]]]:
        matrices = np.rint(
            scipy.spatial.transform.Rotation.create_group("O").as_matrix()
        ).astype(int)

        return [[(matrix @ point) for point in points] for matrix in matrices]

    def find_coords_of_best_orientation(
        self,
        orientations: list[list[tuple[int, int, int]]],
        beacons: set[int, int, int],
    ) -> list[tuple[int, int, int]]:
        for points in orientations:
            offsets = Counter(
                (x1 - x2, y1 - y2, z1 - z2)
                for x1, y1, z1 in points
                for x2, y2, z2 in beacons
            )

            offset, count = offsets.most_common(1)[0]

            if count >= 12:
                self.scanner_coords.add(offset)
                return [
                    tuple(point[i] - offset[i] for i in range(3)) for point in points
                ]
        return None

    def part1(self) -> int:
        beacons = {coord for coord in next(self.data)}

        q = deque(self.all_rotations(points) for points in self.data)

        while q:
            orientations = q.popleft()
            new_coords = self.find_coords_of_best_orientation(orientations, beacons)
            if new_coords:
                beacons |= set(new_coords)
            else:
                q.append(orientations)
        return len(beacons)

    def manhattan(
        self, coord1: tuple[int, int, int], coord2: tuple[int, int, int]
    ) -> int:
        return sum(abs(coord1[i] - coord2[i]) for i in range(len(coord1)))

    def part2(self) -> int:
        return int(
            max(
                self.manhattan(coord1, coord2)
                for coord1, coord2 in itertools.combinations(self.scanner_coords, 2)
            )
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 79 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 3621 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
