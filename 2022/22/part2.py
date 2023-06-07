from collections import defaultdict
from pprint import pprint
import itertools
import pyperclip
import re
import string
import numpy as np
from d3 import Printer

class Position:
    def __init__(self, x: int, y: int, direction: complex, face: str, faces: dict[str, np.ndarray]):
        self.x = x
        self.y = y
        self.direction = direction
        self.face = face
        self.faces = faces
        self._faces_copy = {k: np.copy(v) for k, v in self.faces.items()}
        self.write_new_pos()
        
    def write_new_pos(self):
        sign = ">" if self.direction == 1 + 0j else "<" if self.direction == -1 + 0j else "v" if self.direction == 1j else "^"
        self._faces_copy[self.face][self.y, self.x] = sign
    
    def move(self, distance):
        start_face = self.face
        for _ in range(distance):
            new_pos = self.new_pos()
            if new_pos == (self.x, self.y, self.direction, self.face) or self.faces[new_pos[-1]][new_pos[1], new_pos[0]] == "#":
                break
            self.x, self.y, self.direction, self.face = new_pos
            self.write_new_pos()
        # with open("result.txt", "a") as f:
        #     f.write(f"Distance: {distance}, new_pos: {new_pos}\n")
        #     print(f"Distance: {distance}, new_pos: {new_pos}")
        #     for y in range(self.faces[self.face].shape[1]):
        #         for x in range(self.faces[self.face].shape[0]):
        #             if (x, y) == (self.x, self.y):
        #                 sign = ">" if self.direction == 1 + 0j else "<" if self.direction == -1 + 0j else "v" if self.direction == 1j else "^"
        #                 f.write(sign)
        #                 print(sign, end="")
        #             else:
        #                 f.write(self.faces[self.face][y, x])
        #                 print(self.faces[self.face][y, x], end="")
        #         f.write("\n")
        #         print()
        #     f.write("\n")
        #     print()
        if self.face != start_face:
            pass
            

    def step(self):
        if 0 <= self.x + self.direction.real < self.face.shape[0] and 0 <= self.y + self.direction.imag < self.face.shape[1]:
            if self.face[self.x + self.direction.real, self.y + self.direction.imag] == "#":
                return False
            self.x += self.direction.real
            self.y += self.direction.imag
            return True
        
        raise ValueError("Invalid move")
    
    def rotate(self, rotation: str):
        if rotation == "R":
            self.direction *= 1j
        elif rotation == "L":
            self.direction *= -1j
        else:
            raise ValueError(f"Invalid rotation: {rotation}")
        self.write_new_pos()
    
    def new_pos(self) -> tuple[int, int, complex, str]:
        size = self.faces[self.face].shape[0]
        if 0 <= self.x + int(self.direction.real) < size and 0 <= self.y + int(self.direction.imag) < size:
            if self.faces[self.face][self.y + int(self.direction.imag), self.x + int(self.direction.real)] == "#":
                return self.x, self.y, self.direction, self.face
            return self.x + int(self.direction.real), self.y + int(self.direction.imag), self.direction, self.face
        match self.face:
            case "TOP":
                if self.x + int(self.direction.real) < 0:
                    return self.y, 0, 0 + 1j, "LEFT"
                if self.x + int(self.direction.real) >= size:
                    return size - self.y - 1, 0, 0 + 1j, "RIGHT"
                if self.y + int(self.direction.imag) < 0:
                    return size - self.x - 1, 0, 0 + 1j, "BACK"
                if self.y + int(self.direction.imag) >= size:
                    return self.x, 0, 0 + 1j, "FRONT"
                raise ValueError("Invalid state")
            case "BOTTOM":
                if self.x + int(self.direction.real) < 0:
                    return size - self.y - 1, size - 1, 0 - 1j, "LEFT"
                if self.x + int(self.direction.real) >= size:
                    return self.y, size - 1, 0 - 1j, "RIGHT"
                if self.y + int(self.direction.imag) < 0:
                    return self.x, size - 1, 0 - 1j, "FRONT"
                if self.y + int(self.direction.imag) >= size:
                    return size - self.x - 1, size - 1, 0 - 1j, "BACK"
                raise ValueError("Invalid state")
            case "LEFT":
                if self.x + int(self.direction.real) < 0:
                    return size - 1, self.y, -1 + 0j, "BACK"
                if self.x + int(self.direction.real) >= size:
                    return 0, self.y, 1 + 0j, "FRONT"
                if self.y + int(self.direction.imag) < 0:
                    return 0, self.x, 1 + 0j, "TOP"
                if self.y + int(self.direction.imag) >= size:
                    return 0, size - self.x - 1, 1 + 0j, "BOTTOM"
                raise ValueError("Invalid state")
            case "RIGHT":
                if self.x + int(self.direction.real) < 0:
                    return size - 1, self.y, -1 + 0j, "FRONT"
                if self.x + int(self.direction.real) >= size:
                    return 0, self.y, 1 + 0j, "BACK"
                if self.y + int(self.direction.imag) < 0:
                    return size - 1, size - self.x - 1, -1 + 0j, "TOP"
                if self.y + int(self.direction.imag) >= size:
                    return size - 1, self.x, -1 + 0j, "BOTTOM"
                raise ValueError("Invalid state")
            case "BACK":
                if self.x + int(self.direction.real) < 0:
                    return size - 1, self.y, -1 + 0j, "RIGHT"
                if self.x + int(self.direction.real) >= size:
                    return 0, self.y, 1 + 0j, "LEFT"
                if self.y + int(self.direction.imag) < 0:
                    return size - self.x - 1, 0, 0 + 1j, "TOP"
                if self.y + int(self.direction.imag) >= size:
                    return size - self.x - 1, size - 1, 0 - 1j, "BOTTOM"
                raise ValueError("Invalid state")
            case "FRONT":
                if self.x + int(self.direction.real) < 0:
                    return size - 1, self.y, -1 + 0j, "LEFT"
                if self.x + int(self.direction.real) >= size:
                    return 0, self.y, 1 + 0j, "RIGHT"
                if self.y + int(self.direction.imag) < 0:
                    return self.x, size - 1, 0 - 1j, "TOP"
                if self.y + int(self.direction.imag) >= size:
                    return self.x, 0, 0 + 1j, "BOTTOM"
                raise ValueError("Invalid state")
        raise ValueError("Invalid state")

class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.commands = open(filename).read().rstrip().split("\n\n")[1]
        self.format_commands()
        # open("result.txt", "w").close()

        
        self.faces = {}
        
        if not self.test:
            self.faces["TOP"] = np.array([list(line) for line in open("faces/top.txt").read().rstrip().split("\n")])
            self.faces["BOTTOM"] = np.array([list(line) for line in open("faces/bottom.txt").read().rstrip().split("\n")])
            self.faces["LEFT"] = np.rot90(np.array([list(line) for line in open("faces/left.txt").read().rstrip().split("\n")]), 1)
            self.faces["RIGHT"] = np.rot90(np.array([list(line) for line in open("faces/right.txt").read().rstrip().split("\n")]), 1)
            self.faces["BACK"] = np.rot90(np.array([list(line) for line in open("faces/back.txt").read().rstrip().split("\n")]), 1)
            self.faces["FRONT"] = np.array([list(line) for line in open("faces/front.txt").read().rstrip().split("\n")])
        else:
            self.faces["TOP"] = np.array([list(line) for line in open("example/top.txt").read().rstrip().split("\n")])
            self.faces["BOTTOM"] = np.array([list(line) for line in open("example/bottom.txt").read().rstrip().split("\n")])
            self.faces["LEFT"] = np.array([list(line) for line in open("example/left.txt").read().rstrip().split("\n")])
            self.faces["RIGHT"] = np.rot90(np.array([list(line) for line in open("example/right.txt").read().rstrip().split("\n")]), 1)
            self.faces["BACK"] = np.array([list(line) for line in open("example/back.txt").read().rstrip().split("\n")])
            self.faces["FRONT"] = np.array([list(line) for line in open("example/front.txt").read().rstrip().split("\n")])

        self.pos = Position(0, 0, 1 + 0j, "TOP", self.faces)
        
    def rotate(self, direction: complex, rotation: str) -> complex:
        if rotation == "R":
            return direction * 1j
        elif rotation == "L":
            return direction * -1j
        else:
            raise ValueError(f"Invalid rotation: {rotation}")

    def format_commands(self):
        commands = re.findall(r"(\d+|\w)", self.commands)
        for i, command in enumerate(commands):
            if i % 2 == 0:
                commands[i] = int(command)
        self.commands = commands
    
    def run(self):
        for command in self.commands:
            # print(command)
            if isinstance(command, str):
                self.pos.rotate(command)
                continue
            self.pos.move(command)
        return self.pos.x, self.pos.y, self.pos.direction, self.pos.face
        
    def part2(self):
        final_state = self.run()
        print(final_state)
        self.pos._faces_copy[final_state[-1]][final_state[1], final_state[0]] = "X"
        Printer.show_sides(self.pos._faces_copy)
        direction_num = 0 if final_state[2] == 1 + 0j else 2 if final_state[2] == -1 + 0j else 1 if final_state[2] == 0 + 1j else 3
        match final_state[-1]:
            case "BOTTOM":
                return (2 * 50 + final_state[1] + 1) * 1000 + (50 + final_state[0] + 1) * 4 + direction_num
            case "LEFT":
                if self.test:
                    return (4 + final_state[1] + 1) * 1000 + (4 + final_state[0] + 1) * 4 + direction_num
            case "TOP":
                return (final_state[1] + 1) * 1000 + (50 + final_state[0] + 1) * 4 + direction_num
            case "FRONT":
                return (50 + final_state[1] + 1) * 1000 + (50 + final_state[0] + 1) * 4 + direction_num
                
            # case "BACK":
            #     direction_num = 0 if final_state[2] == 1 + 0j else 2 if final_state[2] == -1 + 0j else 1 if final_state[2] == 0 + 1j else 3
            #     return (3 * 50 + final_state[0] + 1) * 1000 + (50 - final_state[1]) * 4 + direction_num

        raise ValueError("Not implemented face:", final_state[-1])


def main():
    test = Solution(test=True)
    # print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")
    # quit()
    solution = Solution()
    # part1 = solution.part1()
    # print(f"Part 1: {part1}")
    part2 = solution.part2()
    if part2 == 74288:
        print("THIS IS CORRECT")
    else:
        print("THIS IS WROOONG")
    print(f"Part 2: {part2}")



if __name__ == "__main__":
    main()
