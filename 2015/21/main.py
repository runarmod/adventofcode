import re
import itertools


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        pattern = re.compile(r"\w+ ?\w*: (\d+)")
        hitPoints, damage, armour = map(
            int, pattern.findall(open(filename).read().rstrip())
        )
        self.boss = {"hitPoints": hitPoints, "damage": damage, "armour": armour}
        self.player = {"hitPoints": 100, "damage": 0, "armour": 0}
        self.make_shop()

    def make_shop(self):
        self.weapons = []
        self.armours = [(0, 0, 0)]
        self.rings = [(0, 0, 0), (0, 0, 0)]
        c = 0
        for line in open("shop.txt", "r").read().rstrip().split("\n"):
            if line == "":
                c += 1
                continue
            if ":" in line:
                continue

            pattern = re.compile(r"(\w+)(?: \+\d)? +(\d+) +(\d) +(\d)")
            _, cost, damage, armour = pattern.match(line).groups()
            if c == 0:
                self.weapons.append(tuple(int(i) for i in (cost, damage, armour)))
            elif c == 1:
                self.armours.append(tuple(int(i) for i in (cost, damage, armour)))
            elif c == 2:
                self.rings.append(tuple(int(i) for i in (cost, damage, armour)))
        # print(f"{self.weapons=}\n\n{self.armours=}\n\n{self.rings=}")

    def player_wins_fight(self) -> bool:
        boss = self.boss.copy()
        player = self.player.copy()
        while True:
            boss["hitPoints"] -= max(1, player["damage"] - boss["armour"])
            if boss["hitPoints"] <= 0:
                return True
            player["hitPoints"] -= max(1, boss["damage"] - player["armour"])
            if player["hitPoints"] <= 0:
                return False

    def costs(self):
        for w in self.weapons:
            for a in self.armours:
                for r1, r2 in itertools.combinations(self.rings, 2):
                    cost = sum((w[0], a[0], r1[0], r2[0]))
                    self.player["damage"] = sum((w[1], r1[1], r2[1]))
                    self.player["armour"] = sum((a[2], r1[2], r2[2]))

                    yield {"cost": cost, "win": self.player_wins_fight()}

    def part1(self):
        return min(
            (cost for cost in self.costs() if cost["win"]), key=lambda x: x["cost"]
        )["cost"]

    def part2(self):
        return max(
            (cost for cost in self.costs() if not cost["win"]), key=lambda x: x["cost"]
        )["cost"]


def main():
    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
