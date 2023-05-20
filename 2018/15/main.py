from copy import deepcopy
import itertools
import time
from collections import deque


class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 200
        self.attack = 3

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.hp})"

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def repr_short(self):
        return f"{self.__class__.__name__[0]}({self.hp})"


class Elf(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)


class Goblin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)


def parseData(lines):
    free = set()
    characters = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            match char:
                case "#":
                    continue
                case ".":
                    pass
                case "G":
                    characters.append(Goblin(x, y))
                case "E":
                    characters.append(Elf(x, y))
                case _:
                    raise ValueError(f"Unknown character {char}")
            free.add((x, y))
    return free, characters


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.original_free, self.original_entities = parseData(
            open(filename).read().rstrip().split("\n")
        )

        self.free, self.entities = deepcopy(self.original_free), deepcopy(self.original_entities)
        self.elf_count = sum(isinstance(e, Elf) for e in self.original_entities)

    def entity_in_range(self, entity):
        enemies = {(e.x, e.y) for e in self.entities if not isinstance(e, type(entity))}
        return any(
            (entity.x + dx, entity.y + dy) in enemies
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1))
        )

    def find_nearest(self, entity):
        winning_distance = float("inf")
        visited = set()

        enemies = {(e.x, e.y) for e in self.entities if not isinstance(e, type(entity))}
        friends = {(e.x, e.y) for e in self.entities if isinstance(e, type(entity))}

        reachDirections = ((0, -1), (-1, 0), (1, 0), (0, 1))

        q = deque([(entity.x, entity.y, 0, None)])
        while q:
            x, y, dist, first_step_dir = q.popleft()
            if dist > winning_distance:
                break

            if (x, y) in visited:
                continue

            if (x, y) not in self.free:
                continue

            if (x, y) in friends and (x, y) != (entity.x, entity.y):
                continue

            visited.add((x, y))
            if any((x + dx, y + dy) in enemies for dx, dy in reachDirections):
                winning_distance = dist
                yield (x, y, *first_step_dir)
                continue

            for dx, dy in reachDirections:
                q.append((x + dx, y + dy, dist + 1, first_step_dir or (dx, dy)))

    def move(self, entity) -> bool:
        if self.entity_in_range(entity):
            return False

        nearest_lst = list(self.find_nearest(entity))
        nearest_lst.sort(key=lambda x: (x[1], x[0], x[3], x[2]))
        if not nearest_lst:
            return False

        entity.move(*nearest_lst[0][2:])
        return True

    def run(self, health=3):
        for entity in self.entities:
            if isinstance(entity, Elf):
                entity.attack = health

        for round_nr in itertools.count(start=1):
            visited = set()
            prev_size = len(self.entities)

            while len(visited) < prev_size:
                if result := self.check_done(round_nr):
                    return result

                # Get next entity that has not been visited yet (moved or died)
                entity = next(
                    e for e in sorted(self.entities, key=lambda x: (x.y, x.x)) if e not in visited
                )
                visited.add(entity)

                self.move(entity)
                self.fight(entity, visited)

            self.entities.sort(key=lambda e: (e.y, e.x))

    def check_done(self, round_nr):
        if len({type(e) for e in self.entities}) == 1:
            typ = type(next(iter(self.entities)))
            self.won = typ == Elf and len(self.entities) == self.elf_count
            return (round_nr - 1) * sum(e.hp for e in self.entities)
        return None

    def fight(self, entity, visited):
        if not self.entity_in_range(entity):
            return
        enemies_in_range = self.get_enemies_in_range(entity)
        enemy = enemies_in_range[0]
        enemy.hp -= entity.attack
        if enemy.hp <= 0:
            self.entities.remove(enemy)
            visited.add(enemy)

    def get_enemies_in_range(self, entity):
        enemies_in_range = [
            e
            for e in self.entities
            if not isinstance(e, type(entity)) and abs(e.x - entity.x) + abs(e.y - entity.y) == 1
        ]
        enemies_in_range.sort(key=lambda e: (e.hp, e.y, e.x))
        return enemies_in_range

    def part1(self):
        self.free, self.entities = deepcopy(self.original_free), deepcopy(self.original_entities)
        return self.run()

    def part2(self):
        for i in itertools.count(start=4):
            self.free, self.entities = deepcopy(self.original_free), deepcopy(
                self.original_entities
            )
            res = self.run(i)
            if self.won:
                return res


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
