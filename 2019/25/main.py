import itertools
import re
import time

from IntcodeComputer import IntcodeComputer


class Solution:
    def __init__(self):
        self.data = list(map(int, open("input.txt").read().rstrip().split(",")))

    def optimize_path(self, path, opposite):
        # While there are two opposite directions next to each other, remove them
        while True:
            for i in range(1, len(path) - 1):
                if path[i - 1] in opposite and path[i] == opposite[path[i - 1]]:
                    path = path[: i - 1] + path[i + 1 :]
                    break
            else:
                return path

    def generate_path(self, items, opposite, pressure_plate):
        path = []
        for item, p in items:
            path.extend(p)
            path.append("take " + item)
            path.extend(opposite[direction] for direction in p[::-1])
        path.extend(pressure_plate)

        path = self.optimize_path(path, opposite)
        return path

    def run(self, all_items, pressure_plate):
        directions = ["north", "east", "south", "west"]
        N, E, S, W = directions
        opposite = {N: S, S: N, E: W, W: E}

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
            path = self.generate_path(items, opposite, pressure_plate)

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
    print(f"Part 1: {solution.part1()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
