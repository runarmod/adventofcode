from copy import deepcopy
from typing import List


SPELLS = [
    {"index": 0, "cost": 53, "damage": 4, "hp": 0, "armour": 0, "mana": 0, "turns": 0},
    {"index": 1, "cost": 73, "damage": 2, "hp": 2, "armour": 0, "mana": 0, "turns": 0},
    {"index": 2, "cost": 113, "damage": 0, "hp": 0, "armour": 7, "mana": 0, "turns": 6},
    {"index": 3, "cost": 173, "damage": 3, "hp": 0, "armour": 0, "mana": 0, "turns": 6},
    {
        "index": 4,
        "cost": 229,
        "damage": 0,
        "hp": 0,
        "armour": 0,
        "mana": 101,
        "turns": 5,
    },
]


class Solution:
    def __init__(self):
        self.BOSS_DAMAGE = 9

    def reset(self):
        self.record = float("inf")

    def simulate(
        self,
        boss_hp: int,
        player_hp: int,
        player_mana: int,
        active_spells: List = None,
        player_turn: bool = True,
        mana_used: int = 0,
        part: int = 1,
    ):
        if active_spells is None:
            active_spells = []

        if part == 2 and player_turn:
            player_hp -= 1
            if player_hp <= 0:
                return False

        player_armour = 0

        newActiveSpells = []
        for spell in active_spells:
            if spell["turns"] >= 0:
                boss_hp -= spell["damage"]
                player_hp += spell["hp"]
                player_armour += spell["armour"]
                player_mana += spell["mana"]

            newSpell = deepcopy(spell)
            newSpell["turns"] -= 1
            if newSpell["turns"] > 0:
                newActiveSpells.append(newSpell)

        if boss_hp <= 0:
            self.record = min(self.record, mana_used)
            return

        if mana_used >= self.record:
            return

        if player_turn:
            return self.playerPlay(
                boss_hp, player_hp, player_mana, mana_used, part, newActiveSpells
            )

        self.boss_play(
            boss_hp,
            player_hp,
            player_mana,
            mana_used,
            part,
            player_armour,
            newActiveSpells,
        )

    def boss_play(
        self,
        boss_hp,
        player_hp,
        player_mana,
        mana_used,
        part,
        player_armour,
        newActiveSpells,
    ):
        player_hp -= max(1, self.BOSS_DAMAGE - player_armour)
        if player_hp > 0:
            self.simulate(
                boss_hp,
                player_hp,
                player_mana,
                newActiveSpells,
                True,
                mana_used,
                part,
            )

    def playerPlay(
        self, boss_hp, player_hp, player_mana, mana_used, part, newActiveSpells
    ):
        for spell in SPELLS:
            spell_active = any(
                spell2["index"] == spell["index"] for spell2 in newActiveSpells
            )

            cost = spell["cost"]
            if cost <= player_mana and not spell_active:
                self.simulate(
                    boss_hp,
                    player_hp,
                    player_mana - cost,
                    newActiveSpells + [spell],
                    False,
                    mana_used + cost,
                    part,
                )
        return

    def run(self, part):
        self.reset()
        self.simulate(51, 50, 500, part=part)
        return self.record

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)


def main():
    solution = Solution()
    print(part1 := f"Part 1: {solution.part1()}")
    print(part2 := f"Part 2: {solution.part2()}")

    with open("solution.txt", "w") as f:
        f.write(f"{part1}\n{part2}\n")


if __name__ == "__main__":
    main()
