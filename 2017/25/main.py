import re
from collections import defaultdict


"""
Apparantly could have used a YAML parser
"""


def parse_input(inn):
    start, *states = inn.split("\n\n")
    beginning_state = ord(start.split("\n")[0].split(" ")[-1][0]) - ord("A")
    steps = int(re.search(r"(\d+)", start)[1])
    items = []
    for i, state in enumerate(states):
        state_name = i
        state = state.split("\n")[1:]
        items.append([])
        for j in range(0, 8, 4):
            write_val = int(re.search(r"(\d+)", state[j + 1])[0])
            direction = 1 if "right" in state[j + 2] else -1
            next_state = ord(state[j + 3].split(" ")[-1][0]) - ord("A")

            items[state_name].append((write_val, direction, next_state))
    return beginning_state, steps, items


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"

        self.beginning_state, self.steps, self.items = parse_input(open(filename).read().rstrip())

    def part1(self):
        strip = defaultdict(lambda: 0)
        state = self.beginning_state
        position = 0
        for _ in range(self.steps):
            _state_dict = self.items[state][strip[position]]
            write_val = _state_dict[0]
            direction = _state_dict[1]
            next_state = _state_dict[2]

            strip[position] = write_val
            position += direction
            state = next_state
        return sum(strip.values())


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")


if __name__ == "__main__":
    main()
