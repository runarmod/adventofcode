from operator import lshift, rshift
import itertools
import time


class Rock:
    def __init__(self, figure: list[int], i: int, position: int = 0b0010000):
        self.figure = figure
        self.index = i
        self.position = position
        self.height = len(figure)

    def shift(self, direction):
        operation = {">": rshift, "<": lshift}[direction]
        return Rock(
            [operation(row, 1) for row in self.figure], self.index, operation(self.position, 1)
        )

    def collision(self, grid):
        return any(my_row & other_row for my_row, other_row in zip(self.figure, grid))

    def will_crash_wall(self, direction):
        wall = {">": 0b1, "<": 0b1000000}[direction]
        return any(row & wall for row in self.figure)


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.instructions = list(enumerate(open(filename).read().rstrip()))
        self.SHAPES = [
            Rock([0b0011110], 0),
            Rock([0b0001000, 0b0011100, 0b0001000], 1),
            Rock([0b0000100, 0b0000100, 0b0011100], 2),
            Rock([0b0010000, 0b0010000, 0b0010000, 0b0010000], 3),
            Rock([0b0011000, 0b0011000], 4),
        ]

    def run(self, iterations):
        instructions, shapes = itertools.cycle(self.instructions), itertools.cycle(self.SHAPES)
        grid = [0b0] * 50_000
        top = len(grid)
        height = 0

        visited: dict[
            tuple[int, int, int], tuple[int, int]
        ] = {}  # (rock_index, instruction, position) -> (height, iteration)

        instruction = (-1, ">")  # DUMMY

        for rock_nr in itertools.count():
            rock = next(shapes)
            y = top - rock.height - 3

            for y in itertools.count(y):
                instruction = next(instructions)

                if not rock.will_crash_wall(instruction[1]):
                    shifted_rock = rock.shift(instruction[1])
                    if not shifted_rock.collision(grid[y:]):
                        rock = shifted_rock

                if rock.collision(grid[y + 1 :]) or rock.height + y >= len(grid):
                    for i in range(rock.height):
                        grid[y + i] |= rock.figure[i]
                    break

            top = min(top, y)
            height = len(grid) - top

            current_state = (rock.index, instruction[0], rock.position)

            if current_state not in visited:
                visited[current_state] = (height, rock_nr)
                continue

            cycle_size = rock_nr - visited[current_state][1]
            remaining_iterations = iterations - rock_nr - 1
            remaining, remainder = divmod(remaining_iterations, cycle_size)
            if remainder == 0:  # Perfect ending
                cycle_height = height - visited[current_state][0]
                return int(height + cycle_height * remaining)

        return height

    def part1(self):
        return self.run(2022)

    def part2(self):
        return self.run(1e12)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
