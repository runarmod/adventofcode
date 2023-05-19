import functools
import itertools
import os
import re
import string
import sys
import time
from collections import defaultdict, deque
from pprint import pprint
from enum import Enum

sys.path.insert(0, "../../")
from utils import copy_answer, request_submit, write_solution


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    UP = (0, -1)


def parseData(lines):
    carts = []  # One cart is [x, y, direction]
    legal_directions: dict[tuple[int, int], set[Direction]] = {}

    lines = [" " * len(lines[0])] + [f" {line} " for line in lines] + [" " * len(lines[0])]

    for y, line in enumerate(lines):
        for x, v in enumerate(line):
            match v:
                case " ":
                    continue
                case "+":
                    legal_directions[(x, y)] = {
                        Direction.UP,
                        Direction.DOWN,
                        Direction.LEFT,
                        Direction.RIGHT,
                    }
                case "|":
                    legal_directions[(x, y)] = {Direction.UP, Direction.DOWN}
                case "-":
                    legal_directions[(x, y)] = {Direction.LEFT, Direction.RIGHT}
                case "/":
                    if lines[y][x + 1] in "-+><" and lines[y + 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Direction.RIGHT, Direction.DOWN}
                    elif lines[y][x - 1] in "-+><" and lines[y - 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Direction.LEFT, Direction.UP}
                    else:
                        raise RuntimeError("Invalid direction")
                case "\\":
                    if lines[y][x + 1] in "-+><" and lines[y - 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Direction.RIGHT, Direction.UP}
                    elif lines[y][x - 1] in "-+><" and lines[y + 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Direction.LEFT, Direction.DOWN}
                    else:
                        raise RuntimeError("Invalid direction")
                case _:
                    direction = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT][
                        "^>v<".index(v)
                    ]
                    if lines[y][x + 1] in "-+></\\" and lines[y][x - 1] in "-+></\\":
                        legal_directions[(x, y)] = {Direction.LEFT, Direction.RIGHT}
                    elif lines[y + 1][x] in "|+^v/\\" and lines[y - 1][x] in "|+^v/\\":
                        legal_directions[(x, y)] = {Direction.DOWN, Direction.UP}
                    else:
                        raise RuntimeError("Invalid")
                    carts.append([x, y, direction])
    legal_directions = {(k[0] - 1, k[1] - 1): v for k, v in legal_directions.items()}
    carts = [[x - 1, y - 1, direction, 0] for x, y, direction in carts]
    return legal_directions, carts


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.legal_directions, self.carts = parseData(open(filename).read().rstrip().split("\n"))

    def opposite_direction(self, direction):
        match direction:
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.LEFT

        raise RuntimeError("Invalid direction")

    def drive_cart(self, cart):
        new_cart = cart[:]
        direction = new_cart[2]
        dx, dy = direction
        new_cart[0] += dx
        new_cart[1] += dy
        optional_directions = self.legal_directions[(new_cart[0], new_cart[1])].difference(
            {
                self.opposite_direction(direction),
            }
        )

        if len(optional_directions) == 1:
            new_cart[2] = next(iter(optional_directions))
            return new_cart

    def part1(self):
        for _ in itertools.count():
            for cart_index, cart in enumerate(self.carts):
                self.carts[cart_index] = self.drive_cart(cart)
        return None

    def part2(self):
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(part1_text := f"Part 1: {part1}")
    print(part2_text := f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")

    copy_answer(part1, part2)
    write_solution(os.path.dirname(os.path.realpath(__file__)), part1_text, part2_text)
    request_submit(2018, 13, part1, part2)


if __name__ == "__main__":
    main()
