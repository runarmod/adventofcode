from pprint import pprint
import re


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.map, self.commands = open(filename).read().rstrip().split("\n\n")
        self.format_map()
        self.format_commands()
        self.directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        
        self.x = self.map[1].index(".")
        self.y = 1
        self.dir = (1, 0)

    def turn(self, direction):
        if direction == "L":
            self.dir = self.directions[(self.directions.index(self.dir) - 1) % 4]
        elif direction == "R":
            self.dir = self.directions[(self.directions.index(self.dir) + 1) % 4]
        else:
            raise ValueError("Invalid direction")

    def format_commands(self):
        commands = re.findall(r"(\d+|\w)", self.commands)
        for i, command in enumerate(commands):
            if i % 2 == 0:
                commands[i] = int(command)
        self.commands = commands

    def format_map(self):
        max_len = max(len(x) for x in self.map.split("\n"))
        self.map = (
            [[" " for _ in range(max_len + 2)]]
            + [[" "] + list(x) + [" "] * (max_len - len(x) + 1) for x in self.map.split("\n")]
            + [[" " for _ in range(max_len + 2)]]
        )

    def wrap_around(self):
        if self.map[self.y][self.x] != " ":
            return
        if self.dir[0] == 1:
            for i in range(len(self.map[self.y])):
                if self.map[self.y][i] != " ":
                    self.x = i
                    break
        elif self.dir[0] == -1:
            for i in range(len(self.map[self.y]) - 1, -1, -1):
                if self.map[self.y][i] != " ":
                    self.x = i
                    break
        elif self.dir[1] == 1:
            for i in range(len(self.map)):
                if self.map[i][self.x] != " ":
                    self.y = i
                    break
        elif self.dir[1] == -1:
            for i in range(len(self.map) - 1, -1, -1):
                if self.map[i][self.x] != " ":
                    self.y = i
                    break
        else:
            raise NotImplementedError(pprint(self.dir))

    def part1(self):
        for self.command_nr, command in enumerate(self.commands):
            if isinstance(command, int):
                for _ in range(command):
                    safe_x = self.x
                    safe_y = self.y
                    self.x += self.dir[0]
                    self.y += self.dir[1]
                    self.wrap_around()
                    if self.map[self.y][self.x] == "#":
                        self.x = safe_x
                        self.y = safe_y
                        break
            else:
                self.turn(command)
        return self.y * 1000 + self.x * 4 + self.directions.index(self.dir)


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")


if __name__ == "__main__":
    main()
