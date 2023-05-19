from copy import deepcopy
import time
from enum import Enum


class Dir(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    UP = (0, -1)


def parseData(lines):
    carts = []  # One cart is [x, y, direction, turnCounter, index]
    legal_directions: dict[tuple[int, int], set[Dir]] = {}

    # Pad to not have to deal with index out of bounds
    lines = [" " * len(lines[0])] + [f" {line} " for line in lines] + [" " * len(lines[0])]

    cart_index = 0
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case " ":
                    continue

                case "|":
                    legal_directions[(x, y)] = {Dir.UP, Dir.DOWN}

                case "-":
                    legal_directions[(x, y)] = {Dir.LEFT, Dir.RIGHT}

                case "+":
                    legal_directions[(x, y)] = {
                        Dir.UP,
                        Dir.DOWN,
                        Dir.LEFT,
                        Dir.RIGHT,
                    }

                case "/":
                    if lines[y][x + 1] in "-+><" and lines[y + 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Dir.RIGHT, Dir.DOWN}
                    elif lines[y][x - 1] in "-+><" and lines[y - 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Dir.LEFT, Dir.UP}
                    else:
                        raise RuntimeError("Something is wrong :(")

                case "\\":
                    if lines[y][x + 1] in "-+><" and lines[y - 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Dir.RIGHT, Dir.UP}
                    elif lines[y][x - 1] in "-+><" and lines[y + 1][x] in "|+^v":
                        legal_directions[(x, y)] = {Dir.LEFT, Dir.DOWN}
                    else:
                        raise RuntimeError("Something is wrong :(")

                case _:
                    direction = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT]["^>v<".index(c)]
                    if lines[y][x + 1] in "-+></\\" and lines[y][x - 1] in "-+></\\":
                        legal_directions[(x, y)] = {Dir.LEFT, Dir.RIGHT}
                    elif lines[y + 1][x] in "|+^v/\\" and lines[y - 1][x] in "|+^v/\\":
                        legal_directions[(x, y)] = {Dir.DOWN, Dir.UP}
                    else:
                        raise RuntimeError("Something is wrong :(")

                    carts.append([x, y, direction, 0, cart_index])
                    cart_index += 1

    # Remove padding
    legal_directions = {(k[0] - 1, k[1] - 1): v for k, v in legal_directions.items()}
    carts = [[x - 1, y - 1, direction, turns, index] for x, y, direction, turns, index in carts]

    return legal_directions, carts


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.dir_map, self.carts = parseData(open(filename).read().rstrip().split("\n"))

    def opposite_direction(self, direction):
        return Dir((-direction.value[0], -direction.value[1]))

    def turn_cart(self, cart):
        new_cart = cart[:]
        direction = new_cart[2]
        turn = new_cart[3]
        if turn == 0:
            # Turn left
            new_cart[2] = Dir((direction.value[1], -direction.value[0]))
        elif turn == 2:
            # Turn right
            new_cart[2] = Dir((-direction.value[1], direction.value[0]))

        # Update turn counter
        new_cart[3] = (turn + 1) % 3
        return new_cart

    def drive_cart(self, cart):
        new = cart[:]
        direction = new[2]

        new[0] += direction.value[0]
        new[1] += direction.value[1]

        optional_directions = self.dir_map[(new[0], new[1])].difference(
            {
                self.opposite_direction(direction),
            }
        )

        # If there is only one option, we can just set the direction
        if len(optional_directions) == 1:
            new[2] = next(iter(optional_directions))
            return new

        new = self.turn_cart(new)
        return new

    def get_crashed(self, cart, all_carts):
        return next(
            (other_cart for other_cart in all_carts if cart[:2] == other_cart[:2]),
            None,
        )

    def part1(self):
        carts = deepcopy(self.carts)

        while True:
            for i, cart in enumerate(carts):
                new_cart = self.drive_cart(cart)

                # Get first crash
                if self.get_crashed(new_cart, carts) is not None:
                    return ",".join(map(str, new_cart[:2]))

                # Update cart
                carts[i] = new_cart
            # Keep carts sorted low y first, then low x
            carts.sort(key=lambda x: (x[1], x[0]))

    def part2(self):
        carts = deepcopy(self.carts)

        while len(carts) > 1:
            delete = set()

            for i, cart in enumerate(carts):
                new_cart = self.drive_cart(cart)

                # Keep track of crashed carts
                if (other_cart := self.get_crashed(new_cart, carts)) is not None:
                    delete.add(new_cart[-1])
                    delete.add(other_cart[-1])
                    continue

                carts[i] = new_cart

            # Remove crashed carts
            carts = [cart for cart in carts if cart[-1] not in delete]
            carts.sort(key=lambda x: (x[1], x[0]))
        return ",".join(map(str, carts[0][:2]))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
