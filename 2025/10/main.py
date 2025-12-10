import re
import time
from collections import deque

import z3
from aoc_utils_runarmod import get_data


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = get_data(2025, 10, test=test).strip("\n").split("\n")

    def flicks_to_light_state(self, line):
        goal_lights, *buttons, _ = line.split()
        goal_lights = [int(c == "#") for c in goal_lights[1:-1]]
        buttons = tuple(map(nums, buttons))

        q = deque()
        q.append(([0] * len(goal_lights), 0))
        visited = set()
        while q:
            state, steps = q.popleft()
            if state == goal_lights:
                return steps
            state_t = tuple(state)
            if state_t in visited:
                continue
            visited.add(state_t)
            for button in buttons:
                new_state = state[:]
                for b in button:
                    new_state[b] ^= 1
                q.append((new_state, steps + 1))

    def flicks_to_toggle_count(self, line):
        goal_lights, *buttons, joltages = line.split()

        goal_lights = goal_lights[1:-1]
        buttons = tuple(map(nums, buttons))
        joltages = tuple(nums(joltages))

        s = z3.Optimize()
        presses = [z3.Int(f"press_{i}") for i in range(len(buttons))]
        for i in range(len(buttons)):
            s.add(presses[i] >= 0)

        for i in range(len(joltages)):
            actual_presses = sum(
                presses[j] for j, btn in enumerate(buttons) if i in btn
            )
            s.add(actual_presses == joltages[i])

        s.minimize(sum(presses))
        assert s.check() == z3.sat

        m = s.model()
        return sum(m[b].as_long() for b in presses)

    def part1(self):
        return sum(map(self.flicks_to_light_state, self.data))

    def part2(self):
        return sum(map(self.flicks_to_toggle_count, self.data))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 7 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 33 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
