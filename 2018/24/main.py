from copy import deepcopy
import re
import time
from collections import namedtuple

from tqdm import trange


def parseLine(line):
    items = line.split(" ")
    group = {
        "units": int(items[0]),
        "hp": int(items[4]),
        "weak": set(),
        "immune": set(),
        "attack_type": None,
        "attack_damage": 0,
        "initiative": int(items[-1]),
    }

    defences = re.findall(r"\((.*?)\)", line)
    if defences:
        defences = defences[0].split("; ")
    for defence in defences:
        if defence.startswith("weak"):
            group["weak"] = defence.split(" ", maxsplit=2)[2].split(", ")
        elif defence.startswith("immune"):
            group["immune"] = defence.split(" ", maxsplit=2)[2].split(", ")

    damage, type = items[-6:-4]
    group["attack_type"] = type
    group["attack_damage"] = int(damage)

    return group


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            [parseLine(line) for line in section.split("\n")[1:]]
            for section in open(filename).read().rstrip().split("\n\n")
        ]

    def get_effective_power(self, group):
        return group["units"] * group["attack_damage"]

    def dmg(self, attacker, defender):
        mod = 1
        if attacker["attack_type"] in defender["immune"]:
            mod = 0
        elif attacker["attack_type"] in defender["weak"]:
            mod = 2
        return self.get_effective_power(attacker) * mod

    def find_target(self, group, system, data, banned_initiatives=set()):
        enemy_system = 1 - system
        enemy_groups = [
            group
            for group in data[enemy_system]
            if group["initiative"] not in banned_initiatives and group["units"] > 0
        ]
        if not enemy_groups:
            return None

        def key(enemy_group):
            return (
                self.dmg(group, enemy_group),
                self.get_effective_power(enemy_group),
                enemy_group["initiative"],
            )

        possibility = max(enemy_groups, key=key)

        return None if self.dmg(group, possibility) == 0 else possibility

    def run(self, boost):  # Returns positive for infection win, negative for immune win
        data = deepcopy(self.data)
        for i in range(len(data[0])):
            data[0][i]["attack_damage"] += boost

        attacks_tuple = namedtuple("Attack", ["system", "attacker", "defender", "initiative"])
        prev = 0
        while any(group["units"] > 0 for group in data[0]) and any(
            group["units"] > 0 for group in data[1]
        ):
            previous_count = sum(group["units"] for group in data[0] + data[1])
            attacks = []

            def group_sort_key(group):
                return (self.get_effective_power(group), group["initiative"])

            for system in range(2):

                groups_sorted = sorted(
                    data[system],
                    key=group_sort_key,
                    reverse=True,
                )

                attacks += self.find_targets(data, attacks_tuple, system, groups_sorted)

            attacks.sort(key=lambda attack: attack.initiative, reverse=True)
            self.make_attacks(data, attacks)

            if previous_count == prev:
                return None
            prev = previous_count

        return sum(group["units"] for group in data[1]) - sum(group["units"] for group in data[0])

    def find_targets(self, data, attacks_tuple, system, groups_sorted):
        attacks = []
        banned_initiatives = set()
        for group in groups_sorted:
            target = self.find_target(group, system, data, banned_initiatives)
            if target is None:
                continue
            target_index = data[1 - system].index(target)
            banned_initiatives.add(target["initiative"])
            attacker_index = data[system].index(group)
            attacks.append(attacks_tuple(system, attacker_index, target_index, group["initiative"]))
        return attacks

    def make_attacks(self, data, attacks):
        for attack in attacks:
            attacker = data[attack.system][attack.attacker]
            if attacker["units"] <= 0:
                continue
            defender = data[1 - attack.system][attack.defender]
            damage = self.dmg(attacker, defender)
            kills = min(defender["units"], damage // defender["hp"])
            data[1 - attack.system][attack.defender]["units"] -= kills

    def part1(self):
        return self.run(boost=0)

    def part2(self):
        for i in trange(1600 if self.test else 100):
            res = self.run(boost=i)
            if res is not None and res < 0:
                return abs(res)
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
