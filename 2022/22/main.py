from collections import defaultdict
from pprint import pprint
import itertools
import pyperclip
import re
import string


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.map, self.commands = open(filename).read().rstrip().split("\n\n")
        self.format_map()
        self.format_commands()
        self.draw_map()
        self.directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def reset(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] in (">", "v", "<", "^"):
                    self.map[i][j] = "."

        self.x = self.map[1].index(".")
        self.y = 1
        self.dir = (1, 0)

    def draw_map(self):
        with open("test.txt", "w") as f:
            for line in self.map:
                f.write("".join(line) + "\n")

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
            + [
                [" "] + list(x) + [" "] * (max_len - len(x) + 1)
                for x in self.map.split("\n")
            ]
            + [[" " for _ in range(max_len + 2)]]
        )

    def run(self, part):
        for self.command_nr, command in enumerate(self.commands):
            if part == 2:
                with open("test.txt", "w") as f:
                    f.write("\n".join("".join(x) for x in self.map))
            if isinstance(command, int):
                for _ in range(command):
                    self.map[self.y][self.x] = (
                        ">"
                        if self.dir[0] == 1
                        else "v"
                        if self.dir[1] == 1
                        else "<"
                        if self.dir[0] == -1
                        else "^"
                    )
                    safe_x = self.x
                    safe_y = self.y
                    if part == 1:
                        self.x += self.dir[0]
                        self.y += self.dir[1]
                        self.wrap_around_part1()
                    else:
                        if not self.wrap_around_part2():
                            self.x += self.dir[0]
                            self.y += self.dir[1]
                    if self.map[self.y][self.x] == "#":
                        self.x = safe_x
                        self.y = safe_y
                        break
            else:
                self.turn(command)
        self.draw_map()
        print(f"{self.x=}, {self.y=}, {self.dir=}")
        return self.y * 1000 + self.x * 4 + self.directions.index(self.dir)

    def wrap_around_part1(self):
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

    def wrap_around_part2(self):
        if self.y < 1:
            pass
        if 0 < self.y < len(self.map) - 1 and 0 < self.x < len(self.map[0]) - 1:
            if (
                self.x % 50 == 1
                and self.dir[0] == 1
                or self.x % 50 == 0
                and self.dir[1] == -1
            ):
                return False
            if (
                self.y % 50 == 1
                and self.dir[1] == 1
                or self.y % 50 == 0
                and self.dir[1] == -1
            ):
                return False
            if self.y % 50 not in (0, 1) and self.x % 50 not in (0, 1):
                return False
            if 51 <= self.x <= 100 and self.dir[1] in (-1, 1):  # MIDDLE UP-DOWN
                if self.map[self.y + self.dir[1]][self.x + self.dir[0]] != " ":
                    return False

                self.x += self.dir[0]
                self.y += self.dir[1]
                if self.dir[1] == 1:  # DOWN
                    for i in range(len(self.map)):
                        if self.map[i][self.x] != " ":
                            self.y = i

                            return True
                elif self.dir[1] == -1:  # UP
                    for i in range(len(self.map) - 1, -1, -1):
                        if self.map[i][self.x] != " ":
                            self.y = i
                            return True
        if 1 <= self.y <= 50 and self.dir[0] in (1, -1):  # TOP LEFT-RIGHT
            if self.x > 1 and self.dir[0] == -1:
                return False
            if self.x < 150 and self.dir[0] == 1:
                return False
        if self.x <= 50:  # TOP LEFT
            if self.dir[0] == -1:  # TO THE LEFT
                self.x = 51
                self.y = 151 - self.y
                self.dir = (1, 0)

                return True
            elif self.dir[1] == -1:  # UP
                self.y = self.x + 150
                self.x = 51
                self.dir = (1, 0)

                return True
            elif self.dir[1] == 1:  # DOWN
                self.y = 101 - self.x
                self.x = 51
                self.dir = (1, 0)

                return True
            raise NotImplementedError("WTF")
        elif self.x >= 101:  # TOP RIGHT
            if self.dir[0] == 1:  # TO THE RIGHT
                self.x = 100
                self.y = 151 - self.y
                self.dir = (-1, 0)

                return True
            elif self.dir[1] == -1:  # UP
                self.y = 301 - self.x
                self.x = 100
                self.dir = (-1, 0)

                return True
            elif self.dir[1] == 1:  # DOWN
                self.y = self.x - 50
                self.x = 100
                self.dir = (1, 0)

                return True
            raise NotImplementedError("WTF")
        elif 101 <= self.y <= 150 and self.dir[0] in (-1, 1):  # NEXT TO BOTTOM
            if self.dir[0] == -1:  # LEFT
                self.x = 1
                self.y = 151 - self.y
                self.dir = (1, 0)

                return True
            elif self.dir[0] == 1:  # RIGHT
                self.x = 150
                self.y = 151 - self.y
                self.dir = (-1, 0)

                return True
            raise NotImplementedError("WTF")
        elif self.y >= 151:  # BOTTOM
            if self.dir[0] == -1:  # LEFT
                self.x = self.y - 150
                self.y = 1
                self.dir = (0, -1)

                return True
            elif self.dir[0] == 1:  # RIGHT
                self.x = 301 - self.y
                self.y = 1
                self.dir = (0, -1)

                return True
            raise NotImplementedError("WTF")
        elif 51 <= self.y <= 100 and self.dir[0] in (-1, 1):  # NEXT TO TOP
            if self.dir[0] == -1:  # LEFT
                self.x = 101 - self.y
                self.y = 50
                self.dir = (0, 1)

                return True
            elif self.dir[0] == 1:  # RIGHT
                self.x = self.y + 50
                self.y = 50
                self.dir = (0, 1)

                return True
            raise NotImplementedError("WTF")
        raise NotImplementedError(f"x: {self.x}, y: {self.y}, dir: {self.dir} WTF?")

    def part1(self):
        self.reset()
        return self.run(1)

    def rearrange_clean_map(self):
        new = [[" " for _ in range(50)] for _ in range(50)]
        for i in range(len(new)):
            for j in range(len(new[i])):
                new[i][j] = self.map[151 + i][1 + j]
                self.map[151 + i][1 + j] = " "
        # Rotate new 90 degrees to the left
        for _ in range(3):
            new = list(zip(*new[::-1]))
        for i in range(len(new)):
            for j in range(len(new[i])):
                self.map[i + 151][j + 51] = new[i][j]

        new = [[" " for _ in range(50)] for _ in range(50)]
        for i in range(len(new)):
            for j in range(len(new[i])):
                new[i][j] = self.map[101 + i][1 + j]
                self.map[101 + i][1 + j] = " "
        # Rotate new 90 degrees to the left
        for _ in range(2):
            new = list(zip(*new[::-1]))
        for i in range(len(new)):
            for j in range(len(new[i])):
                self.map[i + 1][j + 1] = new[i][j]

        with open("out.txt", "w") as f:
            f.write("\n".join("".join(x) for x in self.map))

    def part2(self):
        self.reset()
        self.rearrange_clean_map()
        return self.run(2)


def main():
    # test = Solution(test=True)
    # print(f"(TEST) Part 1: {test.part1()}")
    # print(f"(TEST) Part 2: {test.part2()}")
    # quit()
    solution = Solution()
    part1 = solution.part1()
    print(part1_text := f"Part 1: {part1}")
    part2 = solution.part2()
    print(part2_text := f"Part 2: {part2}")

    copy_answer(part1, part2)

    with open("solution.txt", "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


def copy_answer(part1, part2):
    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)


if __name__ == "__main__":
    main()
