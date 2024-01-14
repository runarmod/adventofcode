from copy import deepcopy
import heapq
import itertools
import os
import sys
import time

sys.path.insert(0, "../../")
from utils import copy_answer, request_submit, write_solution


class QueueElement:
    def __init__(self, positions: dict[tuple[int, int], str], energy_used: int):
        self.positions = positions
        self.energy_used = energy_used
        # self.remaining = self.remaining_energy()

    def get_data(self):
        return self.positions, self.energy_used

    # def remaining_energy(self):
    #     home_x = {"A": 3, "B": 5, "C": 7, "D": 9}
    #     multiplier = {letter: 10**i for i, letter in enumerate("ABCD")}
    #     s = 0
    #     for (x, y), letter in self.positions.items():
    #         if x == home_x[letter]:
    #             continue
    #         length = abs(x - home_x[letter]) + (y - 1) + 2  # width, up, down
    #         s += length * multiplier[letter]
    #     return s

    def __lt__(self, other):
        # return self.energy_used + self.remaining < other.energy_used + other.remaining
        return self.energy_used < other.energy_used


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.lines = open(filename).read().rstrip().split("\n")
        self.clear, self.positions, self.max_y = self.parse_lines()
        self.coloums = range(3, 10, 2)

    def parse_lines(self):
        clear: set[tuple[int, int]] = set()
        positions: dict[tuple[int, int], str] = dict()

        for y in range(len(self.lines)):
            for x in range(len(self.lines[y])):
                if self.lines[y][x] not in " #":
                    clear.add((x, y))
                if self.lines[y][x] in "ABCD":
                    positions[(x, y)] = self.lines[y][x]
        return clear, positions, len(self.lines) - 2  # Remove bottom + is 0 indexed

    def print_map(self, positions: dict[tuple[int, int], str]):
        for y in range(self.max_y + 2):
            for x in range(13):
                if (x, y) in positions:
                    print(positions[(x, y)], end="")
                elif (x, y) in self.clear:
                    print(".", end="")
                else:
                    print("#", end="")
            print()

    def all_done(self, positions: dict[tuple[int, int], str]):
        if any(coord[1] == 1 for coord in positions):
            return False

        for letter, x in zip("ABCD", self.coloums):
            for coord in positions:
                if positions[coord] == letter and coord[0] != x:
                    return False
        return True

    def home_coords(self, positions: dict[tuple[int, int], str], letter: str):
        x = next(
            itertools.islice(
                self.coloums, "ABCD".index(letter), "ABCD".index(letter) + 1
            )
        )

        y = self.max_y
        if (x, y) not in positions:
            return x, y
        for new_y in range(y - 1, 1, -1):
            if positions[(x, new_y + 1)] != letter:
                return None, None
            if (x, new_y) not in positions:
                return x, new_y
        return None, None

    def route_safe(
        self,
        positions: dict[tuple[int, int], str],
        start: tuple[int, int],
        end: tuple[int, int],
    ):
        start_x, start_y = start
        end_x, end_y = end

        if start_y < end_y:
            dx = -1 if start_x > end_x else 1
            # When we are above where we are going, we move to the side first
            for x in range(start_x + dx, end_x + dx, dx):
                if (x, start_y) in positions:
                    return False
            for y in range(start_y + 1, end_y + 1):
                if (end_x, y) in positions:
                    return False
            return True
        else:
            dx = -1 if start_x > end_x else 1
            # When we are below where we are going, we move up first
            for y in range(start_y - 1, end_y - 1, -1):
                if (end_x, y) in positions:
                    return False
            for x in range(start_x + dx, end_x + dx, dx):
                if (x, end_y) in positions:
                    return False
            return True

    def route_home(self, positions: dict[tuple[int, int], str], coord: tuple[int, int]):
        letter = positions[coord]
        home_coords = self.home_coords(positions, letter)
        if home_coords[0] is None:
            return None, None, None
        assert home_coords[0] is not None and home_coords[1] is not None

        safe = self.route_safe(positions, coord, home_coords)
        if not safe:
            return None, None, None

        energy = self.calculate_energy(
            coord[0], coord[1], home_coords[0], home_coords[1], letter
        )

        return home_coords[0], home_coords[1], energy

    def calculate_energy(self, x1: int, y1: int, x2: int, y2: int, letter: str):
        multiplier: int = 10 ** "ABCD".index(letter)  # A = 1, B = 10, C = 100, D = 1000
        return (abs(x1 - x2) + abs(y1 - y2)) * multiplier

    def locked_home(
        self, letter: str, x: int, y: int, positions: dict[tuple[int, int], str]
    ):
        home_x = next(
            itertools.islice(
                self.coloums, "ABCD".index(letter), "ABCD".index(letter) + 1
            )
        )

        if x != home_x:
            return False

        if y == 1:
            return False

        for tmp_y in range(y + 1, self.max_y + 1):
            if (home_x, tmp_y) in positions and positions[(home_x, tmp_y)] != letter:
                return False
        return True

    def run(self):
        q = [QueueElement(deepcopy(self.positions), 0)]  # positions, steps_taken
        seen = set()

        while q:
            positions, energy_used = heapq.heappop(q).get_data()
            if self.all_done(positions):
                self.print_map(positions)
                return energy_used

            state = tuple(sorted(positions.items()))
            if state in seen:
                continue
            seen.add(state)

            for (x, y), letter in positions.items():
                if self.locked_home(letter, x, y, positions):
                    continue

                if y == 1:
                    available_spot_x, available_spot_y, energy = self.route_home(
                        positions, (x, y)
                    )

                    if energy is not None:
                        new_positions = deepcopy(positions)
                        del new_positions[(x, y)]
                        new_positions[(available_spot_x, available_spot_y)] = letter
                        heapq.heappush(
                            q, QueueElement(new_positions, energy_used + energy)
                        )
                else:
                    possible_xs = set(range(1, 12)).difference(self.coloums)
                    new_y = 1
                    for new_x in possible_xs:
                        if (new_x, new_y) not in positions:
                            if self.route_safe(positions, (x, y), (new_x, new_y)):
                                energy = self.calculate_energy(
                                    x, y, new_x, new_y, letter
                                )
                                new_positions = deepcopy(positions)
                                del new_positions[(x, y)]
                                new_positions[(new_x, new_y)] = letter
                                heapq.heappush(
                                    q, QueueElement(new_positions, energy_used + energy)
                                )
        return None

    def part1(self):
        return self.run()

    def part2(self):
        return None
        """
        #D#C#B#A#
        #D#B#A#C#
        """
        new_lines = ["  #D#C#B#A#", "  #D#B#A#C#"]
        self.lines = self.lines[:3] + new_lines + self.lines[3:]
        self.clear, self.positions, self.max_y = self.parse_lines()
        return self.run()


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 12521 else 'wrong :('}")
    test2 = test.part2()
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 44169 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    print(part1_text := f"Part 1: {part1}")
    part2 = solution.part2()
    print(part2_text := f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    # if part2 >= 59542:
    #     print("Too high")
    #     quit()

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit(2021, 23, part1, part2)


if __name__ == "__main__":
    main()
