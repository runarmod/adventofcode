from collections import deque
from copy import deepcopy
import itertools
from pprint import pprint
import random
import re
import time

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))
        self.rooms = {}
        self.items = {}
        directions = ["north", "east", "south", "west"]
        N, E, S, W = directions
        self.opposite = {N: S, S: N, E: W, W: E}

    def optimize_path(self, path):
        # While there are two opposite directions next to each other, remove them
        while True:
            for i in range(1, len(path) - 1):
                if (
                    path[i - 1] in self.opposite
                    and path[i] == self.opposite[path[i - 1]]
                ):
                    path = path[: i - 1] + path[i + 1 :]
                    break
            else:
                return path

    def generate_path(self, items, pressure_plate):
        path = []
        for item, p in items:
            path.extend(p)
            path.append("take " + item)
            path.extend(self.opposite[direction] for direction in p[::-1])
        path.extend(pressure_plate)

        path = self.optimize_path(path)
        return path

    def find_rooms(self, current_path: list[str] = None, next_direction: str = None):
        if current_path is None:
            current_path = []
        if current_path and self.opposite[next_direction] == current_path[-1]:
            # We are going back to the previous room
            return

        path = current_path[:]
        computer = IntcodeComputer(self.data)
        if next_direction is not None:
            path.append(next_direction)
        for direction in path:
            computer.input_str(direction)

        room_name_regex = re.compile(r"== (.+) ==")
        items_regex = re.compile(r"Items here:\n(?:- (.+)\n)")
        # All directions where we do not autmatically get sent to another room
        directions_regex = re.compile(r"- (north|east|south|west)(?!.*==)", re.DOTALL)

        buffer = ""
        for c in computer.iter():
            buffer += chr(c)
            if not buffer.endswith("Command?"):
                continue
            room_name = room_name_regex.findall(buffer)[0]
            if room_name in self.rooms:
                buffer = ""
                continue

            self.rooms[room_name] = path
            self.items[room_name] = items_regex.findall(buffer)

            print("Found new room: '" + room_name + "'")
            if room_name == "Pressure-Sensitive Floor":
                return

            directions = directions_regex.findall(buffer)
            for direction in directions:
                self.find_rooms(path, direction)
            break

    def run(self, all_items, pressure_plate):
        bad = {
            "escape pod",  # quits the game
            "infinite loop",  # infinite loop...
            "giant electromagnet",  # stuck
            "photons",  # eaten
            "molten lava",  # burned
            "monolith",  # too heavy on its own
        }

        safe = {k: v for k, v in all_items.items() if k not in bad}

        for items in itertools.chain.from_iterable(
            itertools.combinations(safe.items(), r) for r in range(len(safe), 0, -1)
        ):
            path = self.generate_path(items, pressure_plate)

            s = ""
            computer = IntcodeComputer(self.data)
            computer.input_str("\n".join(path))
            for c in computer.iter():
                if s[-7:] == "lighter" or s[-7:] == "heavier":
                    break
                s += chr(c)
            else:
                return int(re.search(r"\d+", s[-100:]).group())
        return None

    def part1(self):
        directions = ["north", "east", "south", "west"]
        N, E, S, W = directions

        # See map.pdf
        pressure_plate = [E, N, E, N, E, E, S, W, N, W]
        items = {
            "escape pod": [E, S],
            "spool of cat6": [E, N, N],
            "mug": [E, N, E],
            "infinite loop": [E, N, E, N, N],
            "asterisk": [E, N, E, N, N, W],
            "molten lava": [E, N, E, N, N, W, N],
            "monolith": [E, N, E, N, N, W, S],
            "sand": [E, N, E, N, E],
            "prime number": [E, N, E, N, E, S, W],
            "photons": [E, N, E, N, E, E, N],
            "giant electromagnet": [E, N, E, N, E, E],
            "tambourine": [E, N, E, N, E, E, S],
            "festive hat": [E, N, E, N, E, E, S, W],
        }

        return self.run(items, pressure_plate)


def main():
    start = time.perf_counter()

    solution = Solution()
    solution.find_rooms()
    pprint(solution.rooms)
    pprint(solution.items)
    # print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
