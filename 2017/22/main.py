def parse_data(inn):
    for y in range(len(inn)):
        for x in range(len(inn[0])):
            if inn[y][x] == "#":
                yield (x - len(inn[0]) // 2, len(inn) // 2 - y)


"""
POSITIVE DIRECTION IS UP AND RIGHT
"""


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.infected = set(parse_data(open(filename).read().rstrip().split("\n")))
        self.directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def part1(self):
        def change_direction():
            nonlocal direction_index, snake, infected
            if tuple(snake) in infected:
                direction_index = (direction_index + 1) % 4
            else:
                direction_index = (direction_index - 1) % 4

        def toggle_node():
            nonlocal snake, infected
            if tuple(snake) in infected:
                infected.remove(tuple(snake))
                return 0
            infected.add(tuple(snake))
            return 1

        def step():
            nonlocal direction_index, snake
            direction = self.directions[direction_index]
            snake[0] += direction[0]
            snake[1] += direction[1]

        snake = [0, 0]
        direction_index = 0
        infected = self.infected.copy()
        bursts = 0
        for _ in range(10000):
            change_direction()
            bursts += toggle_node()
            step()
        return bursts

    def part2(self):
        def change_direction():
            nonlocal direction_index, snake, grid
            match grid.get(tuple(snake), "C"):
                case "I":
                    direction_index = (direction_index + 1) % 4
                case "F":
                    direction_index = (direction_index + 2) % 4
                case "C":
                    direction_index = (direction_index - 1) % 4
                case "W":
                    pass

        def toggle_node():
            nonlocal snake, grid
            snake_t = tuple(snake)
            match grid.get(snake_t, "C"):
                case "W":
                    grid[snake_t] = "I"
                    return 1
                case "I":
                    grid[snake_t] = "F"
                case "C":
                    grid[snake_t] = "W"
                case "F":
                    del grid[snake_t]
            return 0

        def step():
            nonlocal direction_index, snake
            direction = self.directions[direction_index]
            snake[0] += direction[0]
            snake[1] += direction[1]

        snake = [0, 0]
        direction_index = 0
        grid = {key: "I" for key in self.infected.copy()}
        bursts = 0
        for _ in range(10_000_000):
            change_direction()
            bursts += toggle_node()
            step()
        return bursts


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
