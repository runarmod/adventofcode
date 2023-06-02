import dataclasses
import functools
import re
import time


class Blueprint:
    def __init__(
        self,
        index: int,
        ore_price: tuple[int, int, int],
        clay_price: tuple[int, int, int],
        obsidian_price: tuple[int, int, int],
        geode_price: tuple[int, int, int],
    ):
        self.index = index
        self.ore_price = ore_price
        self.clay_price = clay_price
        self.obsidian_price = obsidian_price
        self.geode_price = geode_price

        self.max_ore_cost = max(
            x[0] for x in (self.ore_price, self.clay_price, self.obsidian_price, self.geode_price)
        )
        self.max_clay_cost = max(
            x[1] for x in (self.ore_price, self.clay_price, self.obsidian_price, self.geode_price)
        )
        self.max_obsidian_cost = max(
            x[2] for x in (self.ore_price, self.clay_price, self.obsidian_price, self.geode_price)
        )


@dataclasses.dataclass
class State:
    minutes: int
    ore: int
    clay: int
    obsidian: int
    geode: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int
    blueprint: Blueprint

    def can_create_geode(self):
        return (
            self.ore >= self.blueprint.geode_price[0]
            and self.clay >= self.blueprint.geode_price[1]
            and self.obsidian >= self.blueprint.geode_price[2]
        )

    def can_create_obsidian(self):
        return (
            self.ore >= self.blueprint.obsidian_price[0]
            and self.clay >= self.blueprint.obsidian_price[1]
            and self.obsidian >= self.blueprint.obsidian_price[2]
        )

    def can_create_clay(self):
        return (
            self.ore >= self.blueprint.clay_price[0]
            and self.clay >= self.blueprint.clay_price[1]
            and self.obsidian >= self.blueprint.clay_price[2]
        )

    def can_create_ore(self):
        return (
            self.ore >= self.blueprint.ore_price[0]
            and self.clay >= self.blueprint.ore_price[1]
            and self.obsidian >= self.blueprint.ore_price[2]
        )

    def step(self):
        self.minutes += 1
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geode += self.geode_robots
        return self

    def create_geode(self):
        self.ore -= self.blueprint.geode_price[0]
        self.clay -= self.blueprint.geode_price[1]
        self.obsidian -= self.blueprint.geode_price[2]
        self.geode_robots += 1
        return self

    def create_obsidian(self):
        self.ore -= self.blueprint.obsidian_price[0]
        self.clay -= self.blueprint.obsidian_price[1]
        self.obsidian -= self.blueprint.obsidian_price[2]
        self.obsidian_robots += 1
        return self

    def create_clay(self):
        self.ore -= self.blueprint.clay_price[0]
        self.clay -= self.blueprint.clay_price[1]
        self.obsidian -= self.blueprint.clay_price[2]
        self.clay_robots += 1
        return self

    def create_ore(self):
        self.ore -= self.blueprint.ore_price[0]
        self.clay -= self.blueprint.ore_price[1]
        self.obsidian -= self.blueprint.ore_price[2]
        self.ore_robots += 1
        return self

    def copy(self):
        return State(
            self.minutes,
            self.ore,
            self.clay,
            self.obsidian,
            self.geode,
            self.ore_robots,
            self.clay_robots,
            self.obsidian_robots,
            self.geode_robots,
            self.blueprint,
        )


def createBlueprint(line: str):
    integers = tuple(map(int, re.findall(r"\d+", line)))
    return Blueprint(
        integers[0],
        (integers[1], 0, 0),
        (integers[2], 0, 0),
        (integers[3], integers[4], 0),
        (integers[5], 0, integers[6]),
    )


class Solution:
    def __init__(self):
        filename = "input.txt"
        self.blueprints = [
            createBlueprint(line) for line in open(filename).read().rstrip().split("\n")
        ]

    def run(
        self,
        state: State,
        ore_allowed: bool,
        clay_allowed: bool,
        obsidian_allowed: bool,
        limit: int,
    ) -> int:
        if state.minutes >= limit:
            return state.geode

        # GREED - do not create anything other if it is possible to create geode
        if state.can_create_geode():
            return self.run(state.step().create_geode(), True, True, True, limit)

        best = 0
        new_ore_allowed = True
        if state.can_create_ore():
            new_ore_allowed = False
            if ore_allowed and state.ore_robots < state.blueprint.max_ore_cost:
                best = max(
                    best,
                    self.run(state.copy().step().create_ore(), True, True, True, limit),
                )

        new_clay_allowed = True
        if state.can_create_clay():
            new_clay_allowed = False
            if clay_allowed and state.clay_robots < state.blueprint.max_clay_cost:
                best = max(
                    best,
                    self.run(state.copy().step().create_clay(), True, True, True, limit),
                )

        new_obsidian_allowed = True
        if state.can_create_obsidian():
            new_obsidian_allowed = False
            if obsidian_allowed and state.obsidian_robots < state.blueprint.max_obsidian_cost:
                best = max(
                    best,
                    self.run(state.copy().step().create_obsidian(), True, True, True, limit),
                )

        return max(
            best,
            self.run(state.step(), new_ore_allowed, new_clay_allowed, new_obsidian_allowed, limit),
        )

    def part1(self):
        return sum(
            self.run(State(0, 0, 0, 0, 0, 1, 0, 0, 0, blueprint), True, True, True, 24)
            * blueprint.index
            for blueprint in self.blueprints
        )

    def part2(self):
        return functools.reduce(
            lambda x, y: x * y,
            (
                self.run(State(0, 0, 0, 0, 0, 1, 0, 0, 0, blueprint), True, True, True, 32)
                for blueprint in self.blueprints[:3]
            ),
            1,
        )


def main():
    start = time.perf_counter()

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
