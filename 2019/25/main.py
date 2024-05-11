import itertools
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

    def generate_path(self, items, endpoint):
        path = []
        for item, p in items:
            path.extend(p)
            path.append("take " + item)
            path.extend(self.opposite[direction] for direction in p[::-1])
        path.extend(endpoint)

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

    def gather_all_items(self, items, security_checkpoint):
        computer = IntcodeComputer(self.data)
        # Create path to all items and the security checkpoint
        path = self.generate_path(items.items(), security_checkpoint)
        computer.input_str("\n".join(path))

        # Execute the path and stop at the security checkpoint
        for _ in computer.iter():
            if len(computer.inputs) == 0:
                break
        return computer

    def run(self, all_items, pressure_plate):
        # Don't know how to generalize the bad items
        # Fortunately, all inputs have the same bad items
        bad = {
            "escape pod",  # quits the game
            "infinite loop",  # infinite loop...
            "giant electromagnet",  # stuck
            "photons",  # eaten
            "molten lava",  # burned
            "monolith",  # too heavy on its own
        }

        safe = {k: v for k, v in all_items.items() if k not in bad}

        checkpoint, last_path = pressure_plate[:-1], pressure_plate[-1]
        computer = self.gather_all_items(safe, checkpoint)

        for items_to_drop in itertools.chain.from_iterable(
            itertools.combinations(safe.keys(), r) for r in range(len(safe))
        ):
            final_commands = [f"drop {item}" for item in items_to_drop]
            final_commands.append(last_path)
            new_computer = computer.copy()
            new_computer.input_str("\n".join(final_commands))

            s = ""
            for c in new_computer.iter():
                if s[-7:] == "lighter" or s[-7:] == "heavier":
                    break
                s += chr(c)
            else:
                return int(re.search(r"\d+", s[-100:]).group())
        return None

    def part1(self):
        self.find_rooms()

        pressure_plate = self.rooms["Pressure-Sensitive Floor"]
        items = {
            item: self.rooms[room]
            for room, items in self.items.items()
            for item in items
        }

        return self.run(items, pressure_plate)


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
